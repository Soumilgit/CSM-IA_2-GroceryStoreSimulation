"""SimPy-based Grocery Store Simulation

This module provides a modern SimPy implementation of the grocery store simulation
with enhanced features and better statistics tracking.
"""

import simpy
import random
from typing import Dict, List, Tuple
import json


class CheckoutLine:
    """A checkout line in the grocery store."""
    
    def __init__(self, env: simpy.Environment, line_type: str, line_id: int):
        """Initialize a checkout line.
        
        Args:
            env: SimPy environment
            line_type: Type of line ('cashier', 'express', 'self_serve')
            line_id: Unique identifier for the line
        """
        self.env = env
        self.line_type = line_type
        self.line_id = line_id
        self.resource = simpy.Resource(env, capacity=1)
        self.customers_served = 0
        self.total_service_time = 0
        self.queue_lengths = []
        
    def get_service_time(self, num_items: int) -> float:
        """Calculate service time based on line type and number of items.
        
        Args:
            num_items: Number of items the customer has
            
        Returns:
            Service time in simulation time units
        """
        if self.line_type == 'cashier':
            return num_items + 7
        elif self.line_type == 'express':
            if num_items > 7:
                # Express line shouldn't accept >7 items, but handle it
                return num_items + 7
            return num_items + 4
        elif self.line_type == 'self_serve':
            return 2 * num_items + 1
        return num_items + 7  # Default
    
    def record_queue_length(self):
        """Record current queue length."""
        self.queue_lengths.append(len(self.resource.queue))


class Customer:
    """A customer in the grocery store."""
    
    def __init__(self, customer_id: int, arrival_time: float, num_items: int):
        """Initialize a customer.
        
        Args:
            customer_id: Unique identifier
            arrival_time: Time when customer arrives
            num_items: Number of items to purchase
        """
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.num_items = num_items
        self.line_join_time = None
        self.service_start_time = None
        self.service_end_time = None
        self.assigned_line = None
        
    def wait_time(self) -> float:
        """Calculate total wait time (time in queue)."""
        if self.service_start_time and self.line_join_time:
            return self.service_start_time - self.line_join_time
        return 0
    
    def total_time(self) -> float:
        """Calculate total time in system (arrival to finish)."""
        if self.service_end_time:
            return self.service_end_time - self.arrival_time
        return 0


class GroceryStoreSimPy:
    """SimPy-based grocery store simulation."""
    
    def __init__(self, 
                 num_cashier_lines: int = 2,
                 num_express_lines: int = 1, 
                 num_self_serve_lines: int = 2):
        """Initialize the grocery store.
        
        Args:
            num_cashier_lines: Number of cashier lines
            num_express_lines: Number of express lines
            num_self_serve_lines: Number of self-serve lines
        """
        self.env = simpy.Environment()
        self.lines: List[CheckoutLine] = []
        self.customers: List[Customer] = []
        self.customer_counter = 0
        
        # Create checkout lines
        for i in range(num_cashier_lines):
            self.lines.append(CheckoutLine(self.env, 'cashier', len(self.lines)))
        for i in range(num_express_lines):
            self.lines.append(CheckoutLine(self.env, 'express', len(self.lines)))
        for i in range(num_self_serve_lines):
            self.lines.append(CheckoutLine(self.env, 'self_serve', len(self.lines)))
    
    def find_shortest_line(self, num_items: int) -> CheckoutLine:
        """Find the shortest eligible line for a customer.
        
        Args:
            num_items: Number of items customer has
            
        Returns:
            The shortest eligible checkout line
        """
        eligible_lines = []
        
        # Express lines only for customers with <= 7 items
        if num_items <= 7:
            eligible_lines = [line for line in self.lines]
        else:
            eligible_lines = [line for line in self.lines if line.line_type != 'express']
        
        # Find line with shortest queue
        if eligible_lines:
            return min(eligible_lines, key=lambda line: len(line.resource.queue))
        
        # Fallback to any cashier line
        cashier_lines = [line for line in self.lines if line.line_type == 'cashier']
        return cashier_lines[0] if cashier_lines else self.lines[0]
    
    def customer_process(self, customer: Customer):
        """Process a customer through the store.
        
        Args:
            customer: The customer to process
        """
        # Customer arrives and joins a line
        line = self.find_shortest_line(customer.num_items)
        customer.assigned_line = line
        customer.line_join_time = self.env.now
        
        # Request service from the line
        with line.resource.request() as request:
            yield request
            
            # Service begins
            customer.service_start_time = self.env.now
            service_time = line.get_service_time(customer.num_items)
            
            # Simulate service
            yield self.env.timeout(service_time)
            
            # Service ends
            customer.service_end_time = self.env.now
            line.customers_served += 1
            line.total_service_time += service_time
    
    def customer_generator(self, num_customers: int, arrival_interval: float, 
                          min_items: int = 1, max_items: int = 20):
        """Generate customers arriving at the store.
        
        Args:
            num_customers: Total number of customers to generate
            arrival_interval: Average time between customer arrivals
            min_items: Minimum number of items
            max_items: Maximum number of items
        """
        for i in range(num_customers):
            # Create customer
            num_items = random.randint(min_items, max_items)
            customer = Customer(self.customer_counter, self.env.now, num_items)
            self.customer_counter += 1
            self.customers.append(customer)
            
            # Start customer process
            self.env.process(self.customer_process(customer))
            
            # Wait for next customer (exponential distribution for realistic arrivals)
            if i < num_customers - 1:
                inter_arrival = random.expovariate(1.0 / arrival_interval)
                yield self.env.timeout(inter_arrival)
    
    def monitor_queues(self, interval: float = 1.0, max_recordings: int = 1000):
        """Periodically monitor queue lengths.
        
        Args:
            interval: Time interval between measurements
            max_recordings: Maximum number of recordings to prevent memory issues
        """
        recordings = 0
        while recordings < max_recordings:
            for line in self.lines:
                line.record_queue_length()
            recordings += 1
            yield self.env.timeout(interval)
    
    def run_simulation(self, 
                      num_customers: int = 50,
                      arrival_interval: float = 5.0,
                      min_items: int = 1,
                      max_items: int = 20,
                      random_seed: int = None) -> Dict:
        """Run the simulation and return statistics.
        
        Args:
            num_customers: Number of customers to simulate
            arrival_interval: Average time between arrivals
            min_items: Minimum items per customer
            max_items: Maximum items per customer
            random_seed: Random seed for reproducibility
            
        Returns:
            Dictionary containing simulation statistics
        """
        # Set random seed if provided
        if random_seed is not None:
            random.seed(random_seed)
        
        # Start processes
        self.env.process(self.customer_generator(num_customers, arrival_interval, 
                                                 min_items, max_items))
        self.env.process(self.monitor_queues())
        
        # Run simulation
        self.env.run()
        
        # Calculate statistics
        return self.calculate_statistics()
    
    def calculate_statistics(self) -> Dict:
        """Calculate and return simulation statistics.
        
        Returns:
            Dictionary with various statistics
        """
        completed_customers = [c for c in self.customers if c.service_end_time is not None]
        
        if not completed_customers:
            return {
                'total_customers': len(self.customers),
                'completed_customers': 0,
                'avg_wait_time': 0,
                'max_wait_time': 0,
                'avg_total_time': 0,
                'max_total_time': 0,
                'line_stats': []
            }
        
        wait_times = [c.wait_time() for c in completed_customers]
        total_times = [c.total_time() for c in completed_customers]
        
        line_stats = []
        for line in self.lines:
            avg_queue = sum(line.queue_lengths) / len(line.queue_lengths) if line.queue_lengths else 0
            line_stats.append({
                'line_id': line.line_id,
                'line_type': line.line_type,
                'customers_served': line.customers_served,
                'avg_queue_length': round(avg_queue, 2),
                'max_queue_length': max(line.queue_lengths) if line.queue_lengths else 0,
                'total_service_time': round(line.total_service_time, 2)
            })
        
        return {
            'total_customers': len(self.customers),
            'completed_customers': len(completed_customers),
            'avg_wait_time': round(sum(wait_times) / len(wait_times), 2),
            'max_wait_time': round(max(wait_times), 2),
            'min_wait_time': round(min(wait_times), 2),
            'avg_total_time': round(sum(total_times) / len(total_times), 2),
            'max_total_time': round(max(total_times), 2),
            'min_total_time': round(min(total_times), 2),
            'line_stats': line_stats,
            'simulation_end_time': round(self.env.now, 2)
        }


def run_simulation_wrapper(num_customers: int = 50,
                          arrival_interval: float = 5.0,
                          num_cashier: int = 2,
                          num_express: int = 1,
                          num_self_serve: int = 2,
                          min_items: int = 1,
                          max_items: int = 20,
                          random_seed: int = 42) -> Dict:
    """Wrapper function to run a simulation with given parameters.
    
    This function is designed to be easily called from a UI like Gradio.
    
    Args:
        num_customers: Number of customers to simulate
        arrival_interval: Average time between customer arrivals
        num_cashier: Number of cashier lines
        num_express: Number of express lines
        num_self_serve: Number of self-serve lines
        min_items: Minimum items per customer
        max_items: Maximum items per customer
        random_seed: Random seed for reproducibility
        
    Returns:
        Dictionary containing simulation results
    """
    store = GroceryStoreSimPy(num_cashier, num_express, num_self_serve)
    results = store.run_simulation(num_customers, arrival_interval, 
                                   min_items, max_items, random_seed)
    return results


# Example usage
if __name__ == '__main__':
    print("Running Grocery Store Simulation with SimPy...")
    print("=" * 60)
    
    results = run_simulation_wrapper(
        num_customers=100,
        arrival_interval=3.0,
        num_cashier=2,
        num_express=1,
        num_self_serve=2,
        min_items=1,
        max_items=20,
        random_seed=42
    )
    
    print(f"\nSimulation Results:")
    print(f"Total Customers: {results['total_customers']}")
    print(f"Completed: {results['completed_customers']}")
    print(f"Average Wait Time: {results['avg_wait_time']} units")
    print(f"Maximum Wait Time: {results['max_wait_time']} units")
    print(f"Average Total Time: {results['avg_total_time']} units")
    print(f"Simulation Duration: {results['simulation_end_time']} units")
    
    print(f"\nCheckout Line Statistics:")
    for line_stat in results['line_stats']:
        print(f"\nLine {line_stat['line_id']} ({line_stat['line_type']}):")
        print(f"  Customers Served: {line_stat['customers_served']}")
        print(f"  Avg Queue Length: {line_stat['avg_queue_length']}")
        print(f"  Max Queue Length: {line_stat['max_queue_length']}")

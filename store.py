"""Assignment 1 - Grocery Store Models (Task 1)

This file should contain all of the classes necessary to model the entities
in a grocery store.
"""
# This module is used to read in the data from a json configuration file.

        
import json
from container import PriorityQueue
def get_line_list(c, e, s):
    """ This is a helper function used to get a checkout line list"""
    
    l = []
    for i in range(c):
        l.append(CashierLine())
    for i in range(e):
        l.append(ExpressLine())
    for i in range(s):
        l.append(SelfServeLine())
    return l
    

class GroceryStore:
    """A grocery store.

    A grocery store should contain customers and checkout lines.

    TODO: make sure you update the documentation for this class to include
    a list of all public and private attributes, in the style found in
    the Class Design Recipe.
    === Attributes ===
    @type filename: str
        The name of the file containing the configuration for the
            grocery store.
    """
    def __init__(self, filename):
        """Initialize a GroceryStore from a configuration file <filename>.

        @type filename: str
            The name of the file containing the configuration for the
            grocery store.
        @rtype: None
        """
        with open(filename, 'r') as file:
            config = json.load(file)
        self._line_capacity = config['line_capacity']
        self._express_count = config['express_count']
        self._cashier_count = config['cashier_count']
        self._self_serve_count = config['self_serve_count']
        self._lines = get_line_list(self._cashier_count, self._express_count, self._self_serve_count)
        self._customer_to_line = {}

       
    def assign_customer(self, customer):
        """Assign the customer to the open line with the fewest customers.
        
        Express lines only accept customers with 7 or fewer items.
        Returns the line the customer was assigned to.
        
        @type customer: Customer
        @rtype: Line
        """
        eligible_lines = []
        
        # Determine which lines are eligible
        if customer.number_of_items <= 7:
            # Can use any open line
            eligible_lines = [line for line in self._lines 
                            if line.is_open and line.people_in_line < self._line_capacity]
        else:
            # Cannot use express lines
            eligible_lines = [line for line in self._lines 
                            if line.is_open and 
                            not isinstance(line, ExpressLine) and 
                            line.people_in_line < self._line_capacity]
        
        if not eligible_lines:
            # Fallback: find any open line (shouldn't happen per spec)
            eligible_lines = [line for line in self._lines if line.is_open]
        
        # Find line with fewest customers (lowest index if tie)
        best_line = min(eligible_lines, key=lambda line: line.people_in_line)
        
        # Add customer to line
        best_line.people_in_line += 1
        if best_line.people_in_line > 1:
            # Customer must wait - add to queue
            best_line.queue.append(customer)
        
        return best_line

    def update_customer_to_line(self, customer, line):
        """Update the mapping of customer to their assigned line.
        
        @type customer: Customer
        @type line: Line
        @rtype: None
        """
        self._customer_to_line[customer] = line

    def get_cashier_time(self, n):
        """Calculate checkout time for cashier line.
        
        @type n: int
        @rtype: int
        """
        return n + 7

    def get_express_time(self, n):
        """Calculate checkout time for express line.
        
        @type n: int
        @rtype: int
        """
        return n + 4

    def get_self_serve_time(self, n):
        """Calculate checkout time for self-serve line.
        
        @type n: int
        @rtype: int
        """
        return 2 * n + 1


class Customer:
    """A Customer.

    A Customer has a name( unique string identifier) and number of items
    """
    def __init__(self, name, number_of_items):
        """(Customer,str,int) -> NoneType"""

        self.name = name
        self.number_of_items = number_of_items


class Line:
    """ A Checkout line

    There three types of Checkout lines: Cashier, express and self serve checkout
    Their checkout time for a customer with n items would be: n+7,n+4,2n+1 respectively
    They are referred by unique index(int)
    
    === Attributes ===
    @type people_in_line: int
        Number of people currently in line
    @type queue: list[Customer]
        Queue of customers waiting in line (not including the one being served)
    @type is_open: bool
        Whether the line is open for new customers
    """
    def __init__(self, people_in_line=0):
        self.people_in_line = people_in_line
        self.queue = []
        self.is_open = True


class CashierLine(Line):
    def __init__(self, people_in_line=0):
        super().__init__(people_in_line)


class ExpressLine(Line):
    def __init__(self, people_in_line=0):
        super().__init__(people_in_line)


class SelfServeLine(Line):
    def __init__(self, people_in_line=0):
        super().__init__(people_in_line)


if __name__ == '__main__':
    store = GroceryStore('config.json')



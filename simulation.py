"""Assignment 1 - Grocery Store Simulation (Task 3)

This file should contain all of the classes necessary to model the different
kinds of events in the simulation.
"""
# Feel free to add extra imports here for your own modules.
# Just don't import any external libraries!
from container import PriorityQueue
from store import GroceryStore
from event import Event, create_event_list, EventJoin, EventBegin, EventFinish, EventClose


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    This is the class which is responsible for setting up and running a
    simulation.
    The API is given to you: your main task is to implement the two methods
    according to their docstrings.

    Of course, you may add whatever private attributes and methods you want.
    But because you should not change the interface, you may not add any public
    attributes or methods.

    This is the entry point into your program, and in particular is used for
    autotesting purposes. This makes it ESSENTIAL that you do not change the
    interface in any way!
    """
    # === Private Attributes ===
    # @type _events: PriorityQueue[Event]
    #     A sequence of events arranged in priority determined by the event
    #     sorting order.
    # @type _store: GroceryStore
    #     The grocery store associated with the simulation.
    def __init__(self, store_file):
        """Initialize a GroceryStoreSimulation from a file.

        @type store_file: str
            A file containing the configuration of the grocery store.
        @rtype: None
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, event_file):
        """Run the simulation on the events stored in <event_file>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.

        @type self: GroceryStoreSimulation
        @type event_file: str
            A filename referring to a raw list of events.
            Precondition: the event file is a valid list of events.
        @rtype: dict[str, object]
        """
        # Initialize statistics
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }

        # Track all customers to count unique customers
        all_customers = set()

        # Load initial events from file
        initial_events = create_event_list(event_file)

        # Add all initial events to priority queue
        for event in initial_events:
            self._events.add(event)
            # Count unique customers from initial join events
            if isinstance(event, EventJoin):
                all_customers.add(event.customer)

        # Process events
        while not self._events.is_empty():
            event = self._events.remove()
            
            # Update total_time to be the timestamp of last event
            stats['total_time'] = event.timestamp
            
            # Process the event and get any spawned events
            new_events = event.do(self._store)
            
            # Track customer finish times and calculate wait times
            if isinstance(event, EventFinish):
                customer = event.customer
                if hasattr(customer, 'join_time') and hasattr(customer, 'finish_time'):
                    wait_time = customer.finish_time - customer.join_time
                    if wait_time > stats['max_wait']:
                        stats['max_wait'] = wait_time
            
            # Add spawned events to queue
            if new_events:
                if isinstance(new_events, list):
                    for new_event in new_events:
                        self._events.add(new_event)
                        # Track customers from spawned join events
                        if isinstance(new_event, EventJoin):
                            all_customers.add(new_event.customer)
                else:
                    self._events.add(new_events)
                    if isinstance(new_events, EventJoin):
                        all_customers.add(new_events.customer)

        # Set final customer count
        stats['num_customers'] = len(all_customers)

        return stats


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    sim = GroceryStoreSimulation('config.json')
    final_stats = sim.run('events.txt')
    print(final_stats)

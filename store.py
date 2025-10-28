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
        """assign the customer to the LEGIT line with the fewest number of customers"""
        l, k = [], []
        if customer.number_of_items < 8:
            for line in self._lines:
                l.append(line.people_in_line)
            l.sort()
            for line in self._lines:
                if line.people_in_line == l[0]:
                    line.people_in_line += 1
                    return line

        elif customer.number_of_items >= 8:
            for line in self._lines:
                if not isinstance(line, ExpressLine):
                    k.append(line)
            for item in k:
                l.append(item.people_in_line)
            l.sort()
            for line in k:
                if line.people_in_line == l[0]:
                    line.people_in_line += 1
                    return line

    def update_customer_to_line(self,customer):
        line = self.assign_customer(customer)
        self._customer_to_line[customer] = line


    def get_event(self, filename):
        m = PriorityQueue()
        from event import create_event_list
        for event in create_event_list(filename):
            m.add(event)
        return m

    def get_next_customer(self, queue, customer):
        """ compare customer to the customer in queue
        """

        for i in range(len(queue._items)):
            if queue._items[i] == customer:
                return queue._items[i+1]
            else:
                return None


















    def get_cashier_time(self, n):
        
        return n + 7

    def get_express_time(self, n):
        if n < 8:
            raise Exception('more than 7 items, please go to another line')
        return n+4

    def get_self_serve_time(self, n):

        return 2*n + 1


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
    
    """


class CashierLine(Line):
    def __init__(self, people_in_line=0):

        self.people_in_line = people_in_line


class ExpressLine(Line):
    def __init__(self, people_in_line=0):

        self.people_in_line = people_in_line


class SelfServeLine(Line):
    def __init__(self, people_in_line=0):

        self.people_in_line = people_in_line


if __name__ == '__main__':
    store = GroceryStore('config.json')



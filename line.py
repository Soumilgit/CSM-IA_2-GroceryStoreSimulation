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


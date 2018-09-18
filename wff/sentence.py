""" docstring placeholder """

'''
A sentence is a wff (well formed formula).
'''
from wff.wff import WFF

class Sentence(WFF):
    def __init__(self, time, operator,type_of_operator ,agent ,*args, **kwargs):
        self.time= time
        self.operator=operator # Are our modal operators
        self.type_of_operator=type_of_operator
        self.agent = agent # This defines agent of sentence at time t.
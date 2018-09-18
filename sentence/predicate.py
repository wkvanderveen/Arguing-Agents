'''
Currently using only two terms :
DO, it means agent has done constant.
Capable , it means agent is capable to do whatever is defined in the constant

Predicate is a wff, which means it is a type of sentence.
'''

class Predicate():

    def __init__(self,time, agent, constant = None, term = None, **kwargs):
        self.time = time
        self.agent = agent
        self.constant=constant #Eg. 'let.use.printer' #TODO: in future constant will be replaced by proper structure.
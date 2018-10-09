
'''


types_of_actions = [
    'Buy',
    'Sell'
]

types_of_base = [
    'PriceIsGoingDown', # will have variable as entity
    'AgentIsFree',
    'AgentIsReachable',# if manhatten distance + 2 (for one step of negotiation)is more than global time steps left.
    'HowFarAreAgents', #will have variable as agents
    'AgentHasEntity', # will have variable as entity
    'AgentHasCashForEntity',#will take agent and entity
    'MarketIsClosing',  # will be if global time is left only last 10%
]
'''



'''
Sample Arguments
----------------

Sample actions for A1
Buy(E1,A2), this means buy entity 1 from agent 2
Sell(E2,A3), this means sell entity 2 to agent 3

Valid Argument set for buying E1 from A2 , by A1 - > [
    PriceIsGoingDown(E1)->True,<current price E1>,
    AgentIsFree(A2)-> True,
    AgentIsReachable(A1,A2) -> True, is A1 and A2 can access each other in the left time.
    HowFarAreAgents(A1,A2)->True,<how far in manhattan distance>,
    AgentHasEntity(E1,A2)-> True, (whether A2 has entity E1)
    AgentHasCashForEntity(E1,A1)-> True, (should be >= maximum one unit price of E1 at which agent 1 is willing to buy)
    MarketIsClosing->False (Not necessary because we have implemented agent is reachable.)
    ]
    

Valid Argument set for selling E1 to A2 , by A1- > [
    PriceIsGoingDown(E1)->False,<current price E1>,
    AgentIsFree(A2)-> True,
    AgentIsReachable(A1,A2) -> True, is A1 and A2 can access each other in the left time.
    HowFarAreAgents(A1,A2)->True,<how far in manhattan distance>,
    AgentHasEntity(E1,A1)-> True, (whether A1 has entity E1)
    AgentHasCashForEntity(E1,A2)-> True, (should be >= maximum one unit price of E1 at which agent 2 is willing to buy)
    MarketIsClosing->False (Not necessary because we have implemented agent is reachable.)
    ]
'''

class Action():
    def __int__(self,type_of_action,from_agent,to_agent,entity):
        self.type_of_action=type_of_action #can be "BUY" , "SELL"
        self.from_agent=from_agent
        self.to_agent=to_agent
        self.entity=entity


class ArgumentSet():
    def __init__(self,type_of_action,*args, **kwargs):
        self.type_of_action=type_of_action #Type of action are two , buy or sell.


    def __price_is_going_down(self,entity):
        pass

    def __agent_is_free(self,agent):
        pass

    def __agent_is_reachable(self,agent1,agent2):
        pass

    def __how_far_are_agents(self,agent1,agen2):
        pass

    def __agent_has_entity(self,entity,agent):
        pass

    def __agent_has_cash_for_entity(self):
        pass


#should know all the global variables
class DecisionMakingProcess():

    def __init__(self,asking_agent):
        self.asking_agent=asking_agent


    def create_all_arguments(self):
        self.all_buying_arguments = self.create_buying_arguments_for_agent()
        self.all_selling_arguments = self.create_selling_arguments_for_agent()


    def create_buying_arguments_for_agent(self,agent):
        return []

    def create_selling_arguments_for_agent(self,agent):
        return []


    def filter_out_valid_arguments(self):
        #write lamda function to check if
        #AgentIsFree gives true
        #AgentIsReachable gives true
        #AgentHasEnity
        #AgentHasCashForEntity

        self.valid_arguments=[]

    def resolve_conflict(self):
        pass


    def make_decision(self):
        self.create_all_arguments()
        self.filter_out_valid_arguments()
        decision=self.resolve_conflict() # it will be the action to take.

        return decision



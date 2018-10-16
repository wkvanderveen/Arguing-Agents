
from main import SYSTEM,timesteps
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
    def __init__(self,type_of_action,agent1,agent2,entity):
        self.type_of_action=type_of_action #Type of action are two , buy or sell.
        self.agent1=agent1#This will be asking agent
        self.agent2=agent2
        self.entity=entity



    def __price_is_going_down(self):
        return SYSTEM.is_price_going_down(self.entity.name)

    def __agent_is_free(self):
        return self.agent2.is_agent_free()

    def __agent_is_reachable(self):
        timeleft=timesteps-SYSTEM.time
        manhattan_distance_between_agents=abs(self.agent1.x - self.agent2.x)+abs(self.agent1.y-self.agent2.y)+2
        return timeleft>manhattan_distance_between_agents


    def __how_far_are_agents(self):
        manhattan_distance_between_agents = abs(self.agent1.x - self.agent2.x) + abs(self.agent1.y - self.agent2.y)
        return manhattan_distance_between_agents

    def __agent_has_entity(self):
        if self.type_of_action == 'BUY':
            return (self.agent2.entities_info[self.entity.name]['isInterested'] and
                    self.agent2.entities_info[self.entity.name]['quantity'])
        else:
            return (self.agent1.entities_info[self.entity.name]['isInterested'] and
                    self.agent1.entities_info[self.entity.name]['quantity'])

    def __agent_has_cash_for_entity(self):
        if self.type_of_action == 'BUY':
            agent1_buying_price=self.agent1.get_entity_buying_amount(self.entity.name)
            return  agent1_buying_price and  self.agent1.money >= agent1_buying_price
        else:
            agent2_buying_price = self.agent2.get_entity_buying_amount(self.entity.name)
            return  agent2_buying_price and  self.agent2.money >= agent2_buying_price


#should know all the global variables
class DecisionMakingProcess():

    def __init__(self,asking_agent):
        self.asking_agent=asking_agent


    def create_all_arguments(self):
        self.all_buying_arguments = self.create_buying_arguments_for_agent()
        self.all_selling_arguments = self.create_selling_arguments_for_agent()


    def create_buying_arguments_for_agent(self):
        buying_arguments=[]
        all_other_agents=SYSTEM.get_all_agents_in_list(except_agents=[self.asking_agent])
        all_entities=SYSTEM.get_all_entities()

        for agent in all_other_agents:
            for entity in all_entities:
                buying_arguments.append(ArgumentSet('BUY',self.asking_agent,agent,entity))

        return buying_arguments

    def create_selling_arguments_for_agent(self):
        selling_arguments = []
        all_other_agents = SYSTEM.get_all_agents_in_list(except_agents=[self.asking_agent])
        all_entities = SYSTEM.get_all_entities()

        for agent in all_other_agents:
            for entity in all_entities:
                selling_arguments.append(ArgumentSet('SELL', self.asking_agent, agent, entity))

        return selling_arguments


    def filter_out_valid_arguments(self):
        #write lamda function to check if
        #AgentIsFree gives true
        #AgentIsReachable gives true
        #AgentHasEnity
        #AgentHasCashForEntity

        self.valid_buying_arguments=filter(lambda x: x.__agent_is_free() and
                                                     x.__agent_is_reachable() and x.__agent_has_entity() and x.__agent_has_cash_for_entity()
                                           , self.all_buying_arguments)
        self.valid_selling_arguments=filter(lambda x: x.__agent_is_free() and
                                                     x.__agent_is_reachable() and x.__agent_has_entity() and x.__agent_has_cash_for_entity()
                                           , self.all_selling_arguments)


    def resolve_conflict(self):
        pass


    def make_decision(self):
        self.create_all_arguments()
        self.filter_out_valid_arguments()
        decision=self.resolve_conflict() # it will be the action to take.

        return decision



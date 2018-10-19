
from constants import MAX_TIME as timesteps
from main import SYSTEM

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
    'AgentIsInterestedInEntity', #is agent interested in entity
    'AgentHasEntity', # will have variable as entity
    'AgentHasCashForEntity',#will take agent and entity
    'MarketIsClosing',  # will be if global time is left only last 10%
]

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
    AgentIsInterestedInEntity(A1,E1)-> True if A1 is interested in buying entity E1
    AgentHasEntity(E1,A2)-> True, (whether A2 has entity E1)
    AgentHasCashForEntity(E1,A1)-> True, (should be >= maximum one unit price of E1 at which agent 1 is willing to buy)
    MarketIsClosing->False (Not necessary because we have implemented agent is reachable.)
    ]

Valid Argument set for selling E1 to A2 , by A1- > [
    PriceIsGoingDown(E1)->False,<current price E1>,
    AgentIsFree(A2)-> True,
    AgentIsReachable(A1,A2) -> True, is A1 and A2 can access each other in the left time.
    HowFarAreAgents(A1,A2)->True,<how far in manhattan distance>,
    AgentIsInterestedInEntity(A2,E1)-> True if A2 is interested in buying entity E1
    AgentHasEntity(E1,A1)-> True, (whether A1 has entity E1)
    AgentHasCashForEntity(E1,A2)-> True, (should be >= maximum one unit price of E1 at which agent 2 is willing to buy)
    MarketIsClosing->False (Not necessary because we have implemented agent is reachable.)
    ]
'''


class Action():
    def __init__(self,type_of_action,performed_by_agent,performed_on_agent,entity):
        self.type_of_action=type_of_action #can be "BUY" , "SELL"
        self.performed_by_agent=performed_by_agent
        self.performed_on_agent=performed_on_agent
        self.entity=entity


class ArgumentSet():
    def __init__(self,type_of_action,agent1,agent2,entity):
        self.type_of_action=type_of_action  # Type of action are two , buy or sell.
        self.agent1=agent1  # This will be asking agent
        self.agent2=agent2
        self.entity=entity
        self.score=float('-inf')

    # # Case of can not say will also make argument valid
    # def __price_is_going_up(self):
    #     t=SYSTEM.is_price_going_up(self.entity.name)
    #     return True if t[0] == 'CAN NOT TELL' else t[1]
    #
    #
    # #Case of can not say will also make argument valid
    # def __price_is_going_down(self):
    #     t=SYSTEM.is_price_going_down(self.entity.name)
    #     return True if t[0] == 'CAN NOT TELL' else t[1]

    # Case of can not say will also make argument valid
    def __validity_wrt_price(self):
        if self.type_of_action == 'BUY':
            t = SYSTEM.is_price_going_down(self.entity.name)
        else:
            t = SYSTEM.is_price_going_up(self.entity.name)

        #In order to save recalculation saving it in the argument set itself.
        self.part_0= 1.0 if t[0] == 'CAN TELL' else 0.5 #This is giving more weight to argument in which we can definitly tell to argument in which we can't tell definitly
        return True if t[0] == 'CAN NOT TELL' else t[1]

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
            #In case of buying, whether A1 is interested in Entity, is also taken care of
            agent1_buying_price=self.agent1.get_entity_buying_amount(self.entity.name)
            return  agent1_buying_price and  self.agent1.money >= agent1_buying_price
        else:
            #In case of selling will also take care of whether A2 is interested in Entity
            agent2_buying_price = self.agent2.get_entity_buying_amount(self.entity.name)
            return  agent2_buying_price and  self.agent2.money >= agent2_buying_price

    def is_valid_argument_set(self):
        if self.type_of_action == 'BUY':
            return (self.__validity_wrt_price() and  # price should go down inorder to be it as a buying argument
            self.__agent_is_free() and
            self.__agent_is_reachable() and
            self.__agent_has_entity() and
            self.__agent_has_cash_for_entity())
        else:
            return (    self.__validity_wrt_price() and #price should go up in order to sell
                        self.__agent_is_free() and
                        self.__agent_is_reachable() and
                        self.__agent_has_entity() and
                        self.__agent_has_cash_for_entity())

    #Note: According to the flow this function will be called onlt after filtering of valid arguments.
    def cal_score(self):
        distance =self.__how_far_are_agents() #which will be greater than or equal to zero.
        if distance:
            negotiations=SYSTEM.get_total_negotiation(self.agent1.agent_id,self.agent2.agent_id)
            part_a=(negotiations[1]-negotiations[2])/float(negotiations[0])
            part_b=SYSTEM.get_fraction_change_in_price(self.entity.name)
            part_b*=-1 if self.type_of_action == 'BUY' else part_b
            part_c = 0
            entity_global_avg_price=SYSTEM.get_entity_global_average_price(self.entity.name)

            if self.type_of_action == 'BUY':
                buying_amount=self.agent1.get_entity_buying_amount(self.entity.name)
                if buying_amount !=None and entity_global_avg_price != None and buying_amount!=0:
                    part_c=(buying_amount-entity_global_avg_price)/float(buying_amount)
            else:
                selling_amount=self.agent1.get_entity_selling_amount(self.entity.name)
                if selling_amount != None and entity_global_avg_price != None and selling_amount != 0:
                    part_c=(entity_global_avg_price - selling_amount)/float(selling_amount)

            self.score= (self.part_0+part_a+part_b+part_c)/float(distance)

            self.part_a=part_a
            self.part_b=part_b
            self.part_c=part_c
            self.md=float(distance)


    def __repr__(self):
        return "Action: {}, " \
               "(Asking Agent: {}({},{})), " \
               "(Sent To Agent: {}({},{}))," \
               "Entity: {}, " \
               "Score: {}, " \
               "PartA: {}, " \
               "PartB: {}, " \
               "PartC: {}, " \
               "Distance: {}".format(self.type_of_action,
                                  self.agent1.name,
                                  self.agent1.x,
                                  self.agent1.y,
                                  self.agent2.name,
                                  self.agent2.x,
                                  self.agent2.y,
                                  self.entity.name,
                                  self.score,
                                  self.part_a,
                                  self.part_b,
                                  self.part_c,
                                  self.md
                                  )



#should know all the global variables
class DecisionMakingProcess():

    def __init__(self,asking_agent):
        self.asking_agent=asking_agent
        self.time_point=SYSTEM.time

        print("Initialized DMP For Agent {}, at time {}".format(self.asking_agent.name,self.time_point))


    def create_all_arguments(self):
        self.all_buying_arguments = self.create_buying_arguments_for_agent()
        self.all_selling_arguments = self.create_selling_arguments_for_agent()


    def create_buying_arguments_for_agent(self):
        buying_arguments=[]
        all_other_agents=SYSTEM.get_all_agents_in_list(except_agents=[self.asking_agent.name])
        all_entities=SYSTEM.get_all_entities()

        for agent in all_other_agents:
            for entity in all_entities:
                buying_arguments.append(ArgumentSet('BUY',self.asking_agent,agent,entity))

        return buying_arguments

    def create_selling_arguments_for_agent(self):
        selling_arguments = []
        all_other_agents = SYSTEM.get_all_agents_in_list(except_agents=[self.asking_agent.name])
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
        self.valid_buying_arguments=filter(lambda x: x.is_valid_argument_set(),self.all_buying_arguments)
        self.valid_selling_arguments=filter(lambda x: x.is_valid_argument_set(),self.all_selling_arguments)


    '''
    Note: I am defining dmp as an expert, so it should not have knowledge specific to the agent, which is how many times agent has negotiated with
    other agents and whether it was positive negotiation or negative negotiation.
    By positive I mean agent got what it wanted and negative agent did not get what it wanted.

    Scoring will be done by summing the following:
    1.) (total positive negotiation - total negative negotiation)/Total negotiation
    2.) (Total percentage of local change in price) For definition see time series, in case of buying multiply it by -1 before adding to score
    3.) Total fractional price change wrt agent wrt to entity:
        For buying:
            (maximum buying price - global average price)/maximum buying
        For Selling:
            (global average price - minimum selling price)/minimum selling price

    Final score will be divide it by how far is the agent.
    '''
    def calculate_score_arguments(self,all_arguments):
        for x in all_arguments:
            x.cal_score()

    def resolve_conflict(self):
        all_arguments = list(self.valid_buying_arguments) + list(self.valid_selling_arguments)

        if len(all_arguments)>0:
            self.calculate_score_arguments(all_arguments)
            sorted_arguments=sorted(all_arguments,key=lambda x: x.score,reverse=True)
            wining_argument=sorted_arguments[0]
            for ar in sorted_arguments:
                print(ar.__repr__())
            return wining_argument
        else:
            return None


    def make_decision(self):
        self.create_all_arguments()
        self.filter_out_valid_arguments()
        wining_argument=self.resolve_conflict() # it will be the action to take.
        if wining_argument:
            return Action(wining_argument.type_of_action,wining_argument.agent1,wining_argument.agent2,wining_argument.entity)

        print("****** NO ARGUMENT FOUND *******")
        return None



"""docstring placeholder"""

import pygame
from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants
from random import random, choice, shuffle
import time
import collections
import json
from agent import Agent
from random import randint
from agentstate import NegotiationState,RandomWalkState,WaitForResponseState,WalkToAgentState


class Entity():
    def __init__(self,name):
        self.name=name


#This class will store last three prices of the entity.
class EntityTimeSeries():
    def __init__(self,entity_name):
        self.max_length = 3
        self.entity_name=entity_name
        self.last_prices=collections.deque([], self.max_length) # will only keep last three prices

    def is_price_going_down(self):
        s=zip(list(self.last_prices), list(self.last_prices)[1:])
        l = [x < y for x, y in s]
        return ('CAN TELL',all(l)) if len(l) > 0 else ('CAN NOT TELL',False)

    def is_price_going_up(self):
        s=zip(list(self.last_prices), list(self.last_prices)[1:])
        l=[x<y for x,y in s]
        return ('CAN TELL',all(l)) if len(l)>0 else ('CAN NOT TELL',False)

    def add_price_to_time_series(self,price):
        self.last_prices.append(price)

    '''
    This is fractional local change in price, which means how much price has changed wrt last three points.
    '''
    def get_fraction_change_in_price(self):
        if len(self.last_prices)>0:
            return ((self.last_prices[-1]-self.last_prices[0])/float(sum(self.last_prices)))*len(self.last_prices)
        return 0.0

    def __repr__(self):
        return self.last_prices



#We can convert SYSTEM class to singleton
class System():
    """docstring for System"""


    def __init__(self, display):
        self.time = 0
        self.agents = dict()
        self.display = display

        self.model = GridModel()

        if display:
            pygame.init()
            pygame.display.set_caption("Grid with agents")
            self.view = GridView(self)
            self.control = GridControl(self.model)

        self.entities = [Entity(x) for x in constants.FRUITS]
        self.entity_global_average_price = {}

        self.price_trends={}

        self.total_negotiations =[]

        #This is a dict to maintain price update requests coming from system in the given time step
        self.entity_global_price_updates={}

        print("System initialized.")

    def create_agent(self, name, agent_id, no_agents, x=None, y=None):
        """Create a new Agent in the system."""
        x = randint(0, constants.TILES_X-1) if x == None else x
        y = randint(0, constants.TILES_Y-1) if y == None else x
        new_agent = Agent(name=name,
                          agent_id=agent_id,
                          no_agents=no_agents,
                          x=x,
                          y=y)

        self.agents[name] = new_agent

    def advance(self):
        """Advance the time by a value of 1."""


        requests_sent = 0
        requests_received = 0

        responses_sent = 0
        responses_received = 0

        self.set_global_average_price_for_all_entities() # Update global average price collected in the last step.
        items = list(self.agents.items())
        shuffle(items)

        # Let all agents send their messages
        print("\nSENDING MESSAGES:")
        for name, agent in items:
            agent.send_requests()
            responses_sent += agent.send_responses()

        # Let all agents receive messages
        print("\nRECEIVING MESSAGES:")
        for name, agent in items:
            requests_received += agent.receive_requests()
            responses_received += agent.receive_responses()

        print("\nAGENT INFO:")
        for name, agent in items:
            agent.set_neighbors(self.get_neighbors(agent))
            if isinstance(agent.state, NegotiationState):
                if agent.state.duration > agent.patience:
                    agent.state.decline()
                    continue

                # Accept offer if within price range
                if agent.state.buy_or_sell == 'buy':
                    # if agent.state.price_each <= agent.entities_info['MANGOES']['max_buying_price']:
                    if agent.state.price_each <= agent.entities_info[agent.state.fruit]['max_buying_price']:
                        agent.state.accept()
                        continue
                if agent.state.buy_or_sell == 'sell':
                    # if agent.state.price_each >= agent.entities_info['MANGOES']['min_selling_price']:
                    if agent.state.price_each >= agent.entities_info[agent.state.fruit]['min_selling_price']:
                        agent.state.accept()
                        continue

                # At this point, price should be further negotiated
                if agent.state.buy_or_sell == 'sell':
                    agent.state.price_each -= agent.elasticity*random()/(1+agent.state.duration)
                    agent.state.duration += 1

            elif isinstance(agent.state, RandomWalkState) and not agent.has_incoming_messages():
                agent.random_walk()

            elif isinstance(agent.state, WalkToAgentState) and not agent.has_incoming_messages():
                agent.search_agent(self.find_path(agent))

            elif isinstance(agent.state, WaitForResponseState):
                if agent.state.counter <= 0:
                    agent.state = RandomWalkState(this_agent=agent)
                else:
                    agent.state.counter = agent.state.counter - 1

        for name, agent in self.agents.items():
            agent.set_color()
            agent.state.print_info()
            agent.freeze_movement = False

        self.time += 1

        self.model.update()
        closed = False

        # draw screen
        if self.display:
            self.view.draw()

            # update
            pygame.display.update()
            time.sleep(0.2)
            closed = self.control.check_events()

        return closed

    # set the neighbors of an agent (required for preventing agents from walking through each other)
    def get_neighbors(self, agent):
        neighbors = [None, None, None, None]  # [North, East, South, West]
        for name, possible_neighbor in self.agents.items():
            if possible_neighbor.x == agent.x and possible_neighbor.y == (agent.y - 1):
                neighbors[constants.NORTH] = possible_neighbor
            if possible_neighbor.x == (agent.x + 1) and possible_neighbor.y == agent.y:
                neighbors[constants.EAST] = possible_neighbor
            if possible_neighbor.x == agent.x and possible_neighbor.y == (agent.y + 1):
                neighbors[constants.SOUTH] = possible_neighbor
            if possible_neighbor.x == (agent.x - 1) and possible_neighbor.y == agent.y:
                neighbors[constants.WEST] = possible_neighbor
        return neighbors



    #This will return current global price of the entity
    def get_entity_global_average_price(self,entity_name):
        return self.entity_global_average_price.get(entity_name,None)

    #This will return list of all entities in the System
    def get_all_entities(self):
        return self.entities

    #This will return all agents in a list other than agents in except list
    def get_all_agents_in_list(self,except_agents=[]):
        return [agent for name,agent in self.agents.items() if name not in except_agents]

    #To set global average price of entity
    def update_entity_global_average_price(self,entity_name,price,quantity):
        if entity_name in self.entity_global_price_updates.keys():
            self.entity_global_price_updates[entity_name].append((price,quantity))
        else:
            self.entity_global_price_updates[entity_name]=[(price,quantity)]


    #Should only be called when time step changes
    def set_global_average_price_for_all_entities(self):

        def _weighted_sum(tpls):
            ttl = sum([x[1] for x in tpls])
            return sum([x[0]*x[1] for x in tpls])/ttl

        print("Updating Global Average Prices of Entities ")
        for entity_name, prices in self.entity_global_price_updates.items():
            if len(prices)>0:
                weighted_sum=_weighted_sum(prices)
                gape=(self.entity_global_average_price.get(entity_name,weighted_sum)+weighted_sum)/2
                self.entity_global_average_price[entity_name]=gape
                print("\t Updated average price of entity: "+entity_name,gape)

            #Add average price to entity trend
            temp_price=self.entity_global_average_price.get(entity_name,None)
            if temp_price:
                self.add_price_to_entity_trend(entity_name,temp_price)

        #Reset this when all the calculation are done
        self.reset_enity_global_price_updates_dict()


    def add_price_to_entity_trend(self,entity_name,price):
        entity_trend = self.price_trends.get(entity_name, None)
        if not entity_trend:
            self.price_trends[entity_name] = EntityTimeSeries(entity_name)
            entity_trend = self.price_trends[entity_name]
        entity_trend.add_price_to_time_series(price)

        print("PRICE TRENDS: ")
        self.__print_price_trends()

    def __print_price_trends(self):
        for key,val in self.price_trends.items():
            print(key,val.__repr__())

    def reset_enity_global_price_updates_dict(self):
        self.entity_global_price_updates=dict()


    def is_price_going_up(self,entity_name):
        entity_trend = self.price_trends.get(entity_name,None)
        return entity_trend.is_price_going_up() if entity_trend else ('CAN NOT TELL',False)

    def is_price_going_down(self,entity_name):
        entity_trend = self.price_trends.get(entity_name, None)
        return entity_trend.is_price_going_down() if entity_trend else ('CAN NOT TELL',False)


    def get_fraction_change_in_price(self,entity_name):
        entity_trend = self.price_trends.get(entity_name, None)
        if entity_trend:
            return entity_trend.get_fraction_change_in_price()
        return 0.0






    def agent_at(self, x, y):
        for name, agent in self.agents.items():
            if agent.x == x and agent.y == y:
                return agent
        return None

    def find_path(self, agent):
        target = agent.state.other_agent
        distances = [constants.INF, constants.INF, constants.INF, constants.INF]  # [north, east, south, west]
        directions = []

        distances[constants.NORTH] = self.bfs((agent.x, agent.y - 1), (target.x, target.y))
        distances[constants.EAST] = self.bfs((agent.x + 1, agent.y), (target.x, target.y))
        distances[constants.SOUTH] = self.bfs((agent.x, agent.y + 1), (target.x, target.y))
        distances[constants.WEST] = self.bfs((agent.x - 1, agent.y), (target.x, target.y))

        min_dist = min(distances)

        if min_dist == constants.INF:
            return directions

        if distances[constants.NORTH] == min_dist: directions.append(constants.NORTH)
        if distances[constants.EAST] == min_dist: directions.append(constants.EAST)
        if distances[constants.SOUTH] == min_dist: directions.append(constants.SOUTH)
        if distances[constants.WEST] == min_dist: directions.append(constants.WEST)

        return directions

    def bfs(self, start, end):
        explored = []
        queue = [start]
        levels = {}
        levels[start] = 0
        visited = [start]

        while queue:
            pos = queue.pop(0)
            x = pos[0]
            y = pos[1]
            explored.append(pos)
            neighbors = [(x, y-1), (x+1, y), (x, y+1), (x-1, y)]
            for neighbor in neighbors:
                if neighbor[0] < 0 or neighbor[0] >= constants.TILES_X or neighbor[1] < 0 or neighbor[1] \
                        >= constants.TILES_Y:
                    continue
                if self.agent_at(neighbor[0], neighbor[1]) and not neighbor == end:
                    continue
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.append(neighbor)

                    levels[neighbor] = levels[pos] + 1

        if end not in levels:  # not a single step could have been taken (impossible position)
            return constants.INF
        return levels[end]

    def get_random_target(self, agent_id):
        name, target = choice(list(self.agents.items()))
        while target.agent_id == agent_id:
            name, target = choice(list(self.agents.items()))
        return target

    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))


    '''
    We can keep negotiation count as the property of agent, whcih makes sense, but we are using it as an argument in dmp, so keeping it over here.
    We can change this later.
    '''
    #Initialize total negotiations.
    def initialize_total_negotiations_count(self):
        agents = self.get_all_agents_in_list()
        self.total_negotiations=[[[0,0] for a in agents] for out_a in agents]


    #This will update negotiation count
    def update_negotiation_happened(self,agent1_id,agent2_id,isPositive):
        if isPositive:
            self.total_negotiations[agent1_id][agent2_id][0]+=1
            self.total_negotiations[agent2_id][agent1_id][0] += 1
        else:
            self.total_negotiations[agent1_id][agent2_id][1] += 1
            self.total_negotiations[agent2_id][agent1_id][1] += 1

    def get_total_negotiation(self,agent1_id,agent2_id):
        negotiations=self.total_negotiations[agent1_id][agent2_id]
        return (negotiations[0]+negotiations[1]+1,negotiations[0],negotiations[1]) #This will return total , total positive , total negative




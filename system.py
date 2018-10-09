"""docstring placeholder"""
from agent import *
import pygame
from gridmodel import GridModel
from gridview import GridView
from gridcontrol import GridControl
import constants
import time
import collections

import json


class Entity():
    def __init__(self,name):
        self.name=name


#This class will store last three prices of the entity.
class EntityTimeSeries():
    def __init__(self,entity_name):
        self.max_lenght = 3
        self.entity_name=entity_name
        self.last_prices=collections.deque([], self.max_lenght) # will only keep last three prices

    def is_price_going_down(self):
        s=zip(list(self.last_prices), list(self.last_prices[1:]))
        return all([all(x>y for x, y in s),True if len(s)>0 else False])

    def is_prince_going_up(self):
        s=zip(list(self.last_prices), list(self.last_prices[1:]))
        return all([all(x<y for x, y in s),True if len(s)>0 else False])

    def add_price_to_time_series(self,price):
        self.last_prices.append(price)



#We can convert SYSTEM class to singleton
class System():
    """docstring for System"""


    def __init__(self):
        self.time = 0
        self.agents = dict()

        pygame.init()
        pygame.display.set_caption("Grid with agents")
        self.model = GridModel()
        self.view = GridView(self)
        self.control = GridControl(self.model)

        self.entities = [Entity(x) for x in constants.FRUITS]
        self.entity_global_average_price = {}

        self.price_trends={}

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

        print("\nUpdating system...\n{}\n".format('-' * 56))

        requests_sent = 0
        requests_received = 0

        responses_sent = 0
        responses_received = 0

        self.set_global_average_price_for_all_entities() # Update global average price collected in the last step.

        # Let all agents send their messages
        for name, agent in self.agents.items():
            requests_sent += agent.send_requests()
            responses_sent += agent.send_responses()

        # Let all agents receive messages
        for name, agent in self.agents.items():
            requests_received += agent.receive_requests()
            responses_received += agent.receive_responses()

        for name, agent in self.agents.items():
            agent.set_neighbors(self.get_neighbors(agent))
            if isinstance(agent.state, NegotiationState):
                # TODO: negotiate process
                agent.state.duration += 1

            elif isinstance(agent.state, RandomWalkState):
                agent.random_walk()

            elif isinstance(agent.state, WalkToAgentState):
                agent.search_agent()

        for name, agent in self.agents.items():
            agent.set_color()

        self.time += 1

        # handle input
        crashed = self.control.check_events()

        self.model.update()

        # draw screen
        self.view.draw()

        # update
        pygame.display.update()
        time.sleep(0.2)

        # print(json.dumps(self.price_trends))
        return self.control.check_events()

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
    def update_entity_global_average_price(self,entity_name,price):
        if entity_name in self.entity_global_price_updates.keys():
            self.entity_global_price_updates[entity_name].append(price)
        else:
            self.entity_global_price_updates[entity_name]=[price]


    def set_global_average_price_for_all_entities(self):
        for entity_name, prices in self.entity_global_price_updates.items():
            if len(prices)>0:
                self.entity_global_average_price[entity_name]=(self.entity_global_average_price.get(entity_name,sum(prices)/len(prices))+sum(prices)/len(prices))/2

            #Add average price to entity trend
            temp_price=self.entity_global_average_price.get(entity_name,None)
            if temp_price:
                self.add_price_to_entity_trend(entity_name,temp_price)


        self.reset_enity_global_price_updates_dict()


    def add_price_to_entity_trend(self,entity_name,price):
        entity_trend = self.price_trends.get(entity_name, None)
        if not entity_trend:
            self.price_trends[entity_name] = EntityTimeSeries(entity_name)
            entity_trend = self.price_trends[entity_name]
        entity_trend.add_price_to_time_series(price)


    def reset_enity_global_price_updates_dict(self):
        self.enity_global_price_updates=dict()


    def is_price_going_up(self,entity_name):
        entity_trend = self.price_trends.get(entity_name,None)
        return all(entity_trend,entity_trend.is_prince_going_up())

    def is_price_going_down(self,entity_name):
        entity_trend = self.price_trends.get(entity_name, None)
        return all(entity_trend, entity_trend.is_prince_going_down())








    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))

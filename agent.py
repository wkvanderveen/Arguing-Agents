"""docstring placeholder"""

from message import Request, Response
from agentstate import *
import constants
import json
from random import random, randint, shuffle, uniform


class Agent():
    """docstring for Agent"""
    def __init__(self, name, agent_id, no_agents, x, y, money=0):

        self.name = name
        self.state = RandomWalkState(this_agent=self)
        self.money = money
        self.incoming_requests = []
        self.outgoing_request = None
        self.incoming_responses = []
        self.outgoing_responses = []

        self.x = x
        self.y = y
        self.freeze_movement = False

        self.agent_id = agent_id
        self.no_agents = no_agents

        self.money = constants.MONEY
        self.elasticity = uniform(0, constants.MAX_ELASTICITY)  # more elasticity --> accepting lower price
        self.patience = uniform(0, constants.MAXPATIENCE)  # More patience --> more negotiation steps

        self.entities_info={}

        self.direction = 0

        self.neighbors = [None, None, None, None]

        self.set_color(max_money=constants.MONEY)

        self.set_entities_info()


    def set_entities_info(self):
        from main import SYSTEM
        all_entities = SYSTEM.get_all_entities()
        choices = [True,False]
        for entity in all_entities:

            if True:
                self.set_entity_info(entity)
            else:
                self.entities_info[entity.name] = {'max_buying_price': None ,
                                                   'min_selling_price': None,
                                                   'quantity': None,
                                                   'isInterested': False}

    def set_entity_info(self,entity):
        """Randomly set prices for entities related to agent
        'isInterested' flag tells us that agent is interested in this entity
        """
        self.entities_info[entity.name] = {'max_buying_price': randint(constants.MIN_MAXBUY,
                                                                       constants.MAX_MAXBUY) ,
                                           'min_selling_price': randint(constants.MIN_MINSELL,
                                                                        constants.MAX_MINSELL),
                                           'quantity': randint(constants.MIN_QUANTITY,
                                                               constants.MAX_QUANTITY),
                                           'isInterested': True}


    def search_agent(self, directions):
        if self.adjacent_to_agent(self.state.other_agent):

            entity_name = self.state.action_to_perform.entity.name
            buy_or_sell = self.state.action_to_perform.type_of_action.lower()
            if buy_or_sell == 'buy':
                my_price = int(uniform(self.entities_info[entity_name] \
                        ['max_buying_price'] \
                        * (1-constants.starting_counter_price),
                    self.entities_info[entity_name]['max_buying_price']))
                if self.state.other_agent.entities_info[entity_name]['quantity'] <= 0:
                    self.state = RandomWalkState(self)
                    return
                my_quantity = randint(1, self.state.other_agent.entities_info[entity_name]['quantity'])
            elif buy_or_sell == 'sell':
                my_price = int(uniform(self.entities_info[entity_name] \
                        ['min_selling_price'],
                    self.entities_info[entity_name]['min_selling_price'] * \
                        (1+constants.starting_counter_price)))
                my_quantity = randint(1, self.entities_info[entity_name]['quantity'])

            self.generate_request(request_type=buy_or_sell,
                                  receiver=self.state.other_agent,
                                  fruit=entity_name,
                                  quantity=my_quantity,
                                  price_each=my_price)

        elif not self.move_towards_target(directions):
            self.random_walk()

    def adjacent_to_agent(self, other):
        if (abs(self.x - other.x) + abs(self.y - other.y)) == 1:
            return True
        return False

    def move_towards_target(self, bfs_directions):
        # try to move towards target agent. If not possible, return false
        BFS = True

        if BFS:
            #  random direction from best directions
            indices = list(range((len(bfs_directions))))
            shuffle(indices)
            for index in indices:
                if self.cannot_move(bfs_directions[index]):
                    continue
                dx, dy = self.movement(bfs_directions[index])
                self.x = self.x + dx
                self.y = self.y + dy
                return True
            return False
        else:
            dest_x = self.state.other_agent.x
            dest_y = self.state.other_agent.y

            pref_dir = self.preferred_directions(dest_x, dest_y)
            for direction in pref_dir:
                if self.cannot_move(direction):
                    continue
                dx, dy = self.movement(direction)
                self.x = self.x + dx
                self.y = self.y + dy
                return True
            return False

    def set_target(self, agent):
        self.target_agent = agent

    def preferred_directions(self, dest_x, dest_y):
        pref_dir = []
        if self.x > dest_x:
            # prefer west
            pref_dir.append(constants.WEST)
        elif self.x < dest_x:
            # prefer east
            pref_dir.append(constants.EAST)
        if self.y > dest_y:
            # prefer north
            pref_dir.append(constants.NORTH)
        elif self.y < dest_y:
            # prefer south
            pref_dir.append(constants.SOUTH)
        return pref_dir

    def random_walk(self):
        if self.enclosed():
            return False
        direction = randint(0, 3)
        while self.cannot_move(direction):
            direction = randint(0, 3)
        dx, dy = self.movement(direction)
        self.x = self.x + dx
        self.y = self.y + dy
        return True

    def enclosed(self):
        no_dirs = 4
        for direction in range(4):
            if self.cannot_move(direction):
                no_dirs = no_dirs - 1

        return True if no_dirs == 0 else False

    def cannot_move(self, direction):
        dx, dy = self.movement(direction)
        if (self.x + dx) < 0 or (self.x + dx) >= constants.TILES_X or (self.y + dy) < 0 or (self.y + dy)\
                >= constants.TILES_Y or not self.neighbors[direction] is None:
            return True
        return False

    def set_dir(self, direction):
        self.direction = direction

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors

    def set_color(self, max_money):
        intensity_range = 128
        intensity_step = (intensity_range / max_money) * self.money + 92

        if isinstance(self.state, RandomWalkState):
            color = (0, intensity_step, 0)
        elif isinstance(self.state, WalkToAgentState):
            color = (intensity_step, 0, 0)
        elif isinstance(self.state, NegotiationState):
            color = (0, 0, intensity_step)
        elif isinstance(self.state, WaitForResponseState):
            color = (intensity_step, intensity_step, 0)

        self.color = color

    def get_color(self):
        return self.color

    def get_id(self):
        return self.agent_id

    def get_current_activity(self):
        return self.current_activity

    def movement(self, direction):
        # Do no move if receiving incoming requests
        if self.has_incoming_messages() or self.freeze_movement:
            return 0, 0

        # Do not move if answering 'yes' to a trade request.
        if 'yes' in [x.response_type for x in self.outgoing_responses]:
            return 0, 0

        if direction == constants.NORTH:  # NORTH
            return 0, -1
        elif direction == constants.EAST:  # EAST
            return 1, 0
        elif direction == constants.SOUTH:  # SOUTH
            return 0, 1
        else:  # (3) WEST
            return -1, 0

    def generate_request(self, request_type, receiver, fruit, quantity, price_each):
        """Generate a buy or sell request for an adjacent agent."""
        if isinstance(self.state, WaitForResponseState):
            return

        if isinstance(self.state, NegotiationState):
            return

        msg = Request(sender=self,
                      request_type=request_type,
                      receiver=receiver,
                      fruit=fruit,
                      quantity=quantity,
                      price_each=price_each)

        self.outgoing_request = msg


    def generate_response(self, response_type, receiver, request):
        """Generate an accept or reject response for a requesting agent."""

        # Respond 'no' to every request if already negotiating
        if isinstance(self.state, NegotiationState):
            response_type = 'no'

        msg = Response(sender=self,
                       response_type=response_type,
                       receiver=receiver,
                       request=request)

        self.outgoing_responses.append(msg)

    def send_requests(self):
        """Send generated request to the receiver."""

        # Cannot send requests if agreeing to old request
        if [x.response_type == 'yes' for x in self.outgoing_responses]:
            return

        if self.outgoing_request is not None:
            request = self.outgoing_request

            if not isinstance(request.receiver.state, NegotiationState):
                request.receiver.incoming_requests.append(request)
            self.outgoing_request = None

            self.state = WaitForResponseState(
                this_agent=self,
                other_agent=request.receiver)


    def receive_requests(self):
        """Receive requests from other agents."""
        requests_received = 0

        for request in self.incoming_requests:

            self.incoming_requests.remove(request)
            requests_received += 1

            # Answer 'yes' iff sufficient quantity
            if self.entities_info[request.fruit]['quantity'] >= request.quantity:
                response_type = 'yes'
            else:
                response_type = 'no'

            self.generate_response(response_type=response_type,
                                   receiver=request.sender,
                                   request=request)

            if response_type == 'yes':
                self.freeze_movement = True

        return requests_received

    def send_responses(self):
        """Send all generated responses to the receivers."""
        responses_sent = 0

        for response in self.outgoing_responses:
            self.outgoing_responses.remove(response)
            response.receiver.incoming_responses.append(response)
            responses_sent += 1

            if isinstance(self.state, NegotiationState) or \
               isinstance(response.receiver.state, NegotiationState):
                response.response_type = 'no'

        return responses_sent

    def has_incoming_messages(self):
        return (self.incoming_requests or self.incoming_responses)

    def receive_responses(self):
        """Receive responses from other agents."""
        responses_received = 0

        for response in self.incoming_responses:
            self.incoming_responses.remove(response)
            responses_received += 1
            if not isinstance(self.state, WaitForResponseState):
                continue

            if response.response_type == 'yes':
                if response.request.request_type == 'sell': # agent is buying
                    my_price = int(
                        self.entities_info[response.request.fruit] \
                            ['max_buying_price'] \
                            * uniform((1-self.elasticity),
                                      (1-self.elasticity/2)))

                elif response.request.request_type == 'buy': # agent is selling
                    my_price = int(
                        self.entities_info[response.request.fruit] \
                            ['min_selling_price'] \
                            * uniform(self.elasticity/2+1,
                                      self.elasticity+1))

                self.state = NegotiationState(
                    this_agent=self,
                    buy_or_sell=(
                        'sell' if response.request.request_type == 'buy' \
                        else 'buy'),
                    other_agent=response.sender,
                    quantity=response.request.quantity,
                    fruit=response.request.fruit,
                    price_each=my_price)
                response.sender.state = NegotiationState(
                    this_agent=response.sender,
                    buy_or_sell=response.request.request_type,
                    other_agent=self,
                    quantity=response.request.quantity,
                    fruit=response.request.fruit,
                    price_each=response.request.price_each)
            else:
                self.state = RandomWalkState(this_agent=self)
                break

        return responses_received


    def update_entity_quantity(self, entity_name, quantity):
        self.entities_info[entity_name]['quantity'] = quantity

    def is_agent_free(self):
        """When state of agent is RandomWalk then agent is free."""
        return isinstance(self.state, RandomWalkState)

    """The following 2 functions will return min or max amount of money
    agent has set to sell or buy entity.
    If its not set then None will be returned.
    """
    def get_entity_buying_amount(self, entity_name):
        entity_info = self.entities_info.get(entity_name, None)
        if entity_info:
            return entity_info['max_buying_price']
        return None

    def get_entity_selling_amount(self, entity_name):
        entity_info = self.entities_info.get(entity_name, None)
        if entity_info:
            return entity_info['min_selling_price']
        return None


    #This function will update amount agent will have
    def update_agent_money(self, new_money):
        self.money = new_money


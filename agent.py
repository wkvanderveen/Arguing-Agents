"""docstring placeholder"""
from message import Request, Response
from agentstate import *
import constants
from random import random, randint
import json

class Agent():
    """docstring for Agent"""
    def __init__(self, name, agent_id, no_agents, x, y, money=0):

        self.name = name
        self.state = RandomWalkState(this_agent=self)
        self.money = money
        self.incoming_requests = []
        self.outgoing_requests = []
        self.incoming_responses = []
        self.outgoing_responses = []

        self.x = x
        self.y = y

        self.agent_id = agent_id
        self.no_agents = no_agents

        self.money = constants.MONEY
        self.elasticity = random()  # more elasticity --> accepting lower price
        self.patience = randint(0, constants.MAXPATIENCE)  # More patience --> more negotiation steps

        self.entities_info={}

        self.direction = 0

        self.neighbors = [None, None, None, None]

        self.set_color()

        self.set_entities_info()

        print("Agent '{}' initialized.".format(self.name))
        #print("\t Agent Entity Info" + json.dumps(self.entities_info))


    def set_entities_info(self):
        from main import SYSTEM
        all_entities=SYSTEM.get_all_entities()
        choices=[True,False]
        for entity in all_entities:
            if choices[randint(0,1)]:
                self.set_entity_info(entity)
            else:
                self.entities_info[entity.name]={'max_buying_price': None ,
                                                 'min_selling_price': None,
                                                 'quantity':None,
                                                 'isInterested':False}

    #Randomly set prices for entities related to agent
    #isInterested Flag tell us that agent is interested in this entity
    def set_entity_info(self,entity):
        self.entities_info[entity.name]={'max_buying_price': randint(10, 100) ,
                                         'min_selling_price': randint(10, 100),
                                         'quantity':randint(1, 10),
                                         'isInterested':True}

    def print_info(self):
        """Print the relevant information about this agent."""
        print("This is Agent '{0}' on position {1}.".format(
          self.name,
          self.position))

    def search_agent(self):
        if self.adjacent_to_agent(self.state.other_agent):
            print("Found target")
        elif not self.move_towards_target():
            self.random_walk()

    def adjacent_to_agent(self, other):
        if (abs(self.x - other.x) + abs(self.y - other.y)) == 1:
            return True
        return False

    def move_towards_target(self):
        # try to move towards target agent. If not possible, return false
        bf_search = False

        if bf_search:
            dir = bf_search()

            return True
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

    def set_color(self):
        color_range = 180
        color_step = (color_range / (self.no_agents - 1)) * self.agent_id
        c1 = 65 + color_range - color_step
        color_step = max(color_step - color_range / 2, 0)
        c2 = 255
        c3 = 65 + color_step
        if isinstance(self.state, RandomWalkState):
            color = (c1, c2, c3)
        elif isinstance(self.state, WalkToAgentState):
            color = (c2, 0, 0)
        elif isinstance(self.state, NegotiationState):
            color = (0, 0, c2)
        elif isinstance(self.state, WaitForResponseState):
            color = (128, 128, 128)
        self.color = color

    def get_color(self):
        return self.color

    def get_id(self):
        return self.agent_id

    def get_current_activity(self):
        return self.current_activity

    def movement(self, direction):
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


    def generate_request(self, request_type, receiver, fruit, quantity):
        """Generate a buy or sell request for an adjacent agent."""
        if isinstance(self.state, WaitForResponseState):
            print("Agent {0} cannot send request ".format(self.name) +
                  "because it is already waiting for a response!")
        msg = Request(sender=self,
                      request_type=request_type,
                      receiver=receiver,
                      fruit=fruit,
                      quantity=quantity)

        self.outgoing_requests.append(msg)


    def generate_response(self, response_type, receiver, request):
        """Generate an accept or reject response for a requesting agent."""

        # If already negotiating, respond 'no' to everything
        if isinstance(self.state, NegotiationState):
            response_type = 'no'

        msg = Response(sender=self,
                       response_type=response_type,
                       receiver=receiver,
                       request=request)

        self.outgoing_responses.append(msg)

    def send_requests(self):
        """Send all generated requests to the receivers."""
        requests_sent = 0

        for request in self.outgoing_requests:
            request.on_send()
            self.outgoing_requests.remove(request)
            if isinstance(request.receiver.state, NegotiationState):
                print("Request blocked -- other agent already negotiating!")
            else:
                request.receiver.incoming_requests.append(request)
                requests_sent += 1
            self.state = WaitForResponseState(
                this_agent=self,
                other_agent=request.receiver)

        return requests_sent

    def receive_requests(self):
        """Receive requests from other agents."""
        requests_received = 0

        for request in self.incoming_requests:
            request.on_receive()

            self.incoming_requests.remove(request)
            requests_received += 1

            # TODO: Decision making process to generate response

            ### HARDCODE: ANSWER 'YES' TO REQUEST
            self.generate_response(response_type='yes',
                                   receiver=request.sender,
                                   request=request)
            ###

            # The agent shouldn't move away before answering the request
            self.state = WaitForResponseState(
                this_agent=self,
                other_agent=request.sender)

        return requests_received

    def send_responses(self):
        """Send all generated responses to the receivers."""
        responses_sent = 0

        for response in self.outgoing_responses:
            response.on_send()
            self.outgoing_responses.remove(response)
            response.receiver.incoming_responses.append(response)
            responses_sent += 1

        return responses_sent


    def receive_responses(self):
        """Receive responses from other agents."""
        responses_received = 0

        for response in self.incoming_responses:
            response.on_receive()
            self.incoming_responses.remove(response)
            responses_received += 1

            if response.response_type == 'yes' and \
                isinstance(self.state, WaitForResponseState) and \
                not isinstance(response.sender.state, NegotiationState):
                self.state = NegotiationState(
                    this_agent=self,
                    buy_or_sell=response.request.request_type,
                    other_agent=response.sender)

                response.sender.state = NegotiationState(
                    this_agent=response.sender,
                    buy_or_sell=('sell' if response.request.request_type == 'buy' else 'buy'),
                    other_agent=self)

        return responses_received

from random import randint
from random import random
from basket import Basket
import constants


class Agent():
    def __init__(self, x, y, agent_id, no_agents):
        self.x = x
        self.y = y
        self.agent_id = agent_id
        self.no_agents = no_agents

        self.money = constants.MONEY
        self.elasticity = random()  # more elasticity --> accepting lower price
        self.patience = randint(0, constants.MAXPATIENCE)  # More patience --> more negotiation steps
        self.basket = Basket()

        self.current_activity = constants.RANDOM_WALK
        self.direction = 0
        self.target_agent = None
        self.trade_partner = None

        self.neighbors = [None, None, None, None]

        self.set_color()

    def update(self, rand_targ): # TODO: remove random target
        if self.current_activity == constants.RANDOM_WALK:
            self.random_walk()
            if random() < 0.01:
                # TODO: now randomly assigns target
                self.set_random_target(rand_targ)
        elif self.current_activity == constants.SEARCH_AGENT:
            self.search_agent()
        elif self.current_activity == constants.NEGOTIATE:
            self.negotiate()
            # TODO now randomly stops negotiation
            if random() < 0.001:
                self.stop_negotiation()

        self.set_color()

    def set_random_target(self, target):
        self.current_activity = constants.SEARCH_AGENT
        self.target_agent = target

    def negotiate(self):
        if self.adjacent_to_agent(self.trade_partner):
            print("request sent from agent " + str(self.get_id()) + " to agent " + str(self.trade_partner.get_id()) + "...")
            print("response from agent " + str(self.trade_partner.get_id()) + ": " + self.trade_partner.request(self))
        else:
            self.current_activity = constants.RANDOM_WALK
            self.random_walk()

    def stop_negotiation(self):
        self.agree_to_stop_negotiation(self.trade_partner)
        self.leave_negotiation()

    def leave_negotiation(self):
        self.current_activity = constants.RANDOM_WALK
        self.trade_partner = None
        self.target_agent = None

    #  -------------------------------------
    #  ----- received from other agent -----
    def agree_to_stop_negotiation(self, other_agent):
        self.leave_negotiation()

    def accepts_request(self, other_agent):
        if self.current_activity == constants.NEGOTIATE:
            return False
        self.current_activity = constants.NEGOTIATE
        self.trade_partner = other_agent
        return True

    @staticmethod
    def request(other_agent):
        return "hello agent " + str(other_agent.get_id())
    #  ----- received from other agent -----
    #  -------------------------------------

    def search_agent(self):
        if self.target_agent is None:
            self.current_activity = constants.RANDOM_WALK
            return False
        if self.adjacent_to_agent(self.target_agent):
            print("Found target")
            self.start_negotiate()
        elif not self.move_towards_target():
            self.random_walk()

    def start_negotiate(self):
        self.current_activity = constants.NEGOTIATE
        self.trade_partner = self.target_agent
        self.target_agent = None
        if self.trade_partner.accepts_request(self):
            self.negotiate()
        else:
            self.trade_partner = None
            self.current_activity = constants.RANDOM_WALK

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
            dest_x = self.target_agent.x
            dest_y = self.target_agent.y

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
        if self.current_activity == constants.RANDOM_WALK:
            color = (c1, c2, c3)
        elif self.current_activity == constants.SEARCH_AGENT:
            color = (c2, 0, 0)
        elif self.current_activity == constants.NEGOTIATE:
            color = (0, 0, c2)
        self.color = color

    def get_color(self):
        return self.color

    def get_id(self):
        return self.agent_id

    def get_current_activity(self):
        return self.current_activity

    @staticmethod
    def movement(direction):
        if direction == constants.NORTH:  # NORTH
            return 0, -1
        elif direction == constants.EAST:  # EAST
            return 1, 0
        elif direction == constants.SOUTH:  # SOUTH
            return 0, 1
        else:  # (3) WEST
            return -1, 0

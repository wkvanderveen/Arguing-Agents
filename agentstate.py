mapping={'buy':'bought','sell':'sold'}
class AgentState(object):
    def __init__(self, this_agent, *args, **kwargs):
        self.this_agent = this_agent

class NegotiationState(AgentState):
    """docstring for NegotiationState"""
    def __init__(self, buy_or_sell, other_agent, fruit, quantity, price_each, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buy_or_sell = buy_or_sell
        self.other_agent = other_agent
        self.fruit = fruit
        self.quantity = quantity
        self.duration = 0
        self.price_each = price_each

    def decline(self):
        from main import SYSTEM
        self.other_agent.state = RandomWalkState(this_agent=self.other_agent)
        self.this_agent.state = RandomWalkState(this_agent=self.this_agent)
        # print("Trade cancelled between agent {0} and agent {1} after {2} turn{3}.".format(
        #     self.this_agent.name,
        #     self.other_agent.name,
        #     self.duration,
        #     ('' if self.duration == 1 else 's')))
        SYSTEM.update_negotiation_happened(self.this_agent.agent_id,self.other_agent.agent_id,False) #This means negative negotiation happend


    def accept(self):
        from main import SYSTEM
        transaction_money = self.price_each * self.quantity

        self.this_agent.money -= transaction_money
        self.this_agent.entities_info[self.fruit]['quantity'] += self.quantity
        self.other_agent.money+=transaction_money
        self.other_agent.entities_info[self.fruit]['quantity'] -= self.quantity

        self.other_agent.state = RandomWalkState(this_agent=self.other_agent)
        self.this_agent.state = RandomWalkState(this_agent=self.this_agent)

        SYSTEM.update_negotiation_happened(self.this_agent.agent_id, self.other_agent.agent_id,
                                           True)  # This means positive negotiation happend

        SYSTEM.update_entity_global_average_price(self.fruit,self.price_each,self.quantity)

    def print_info(self):
        print("Agent {0} is {1} agent {2} for {3} steps so far.".format(
            self.this_agent.name,
            ('selling to' if self.buy_or_sell == 'sell' else 'buying from'),
            self.other_agent.name,
            self.duration))

class WalkToAgentState(AgentState):
    def __init__(self, other_agent, action_to_perform,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_agent = other_agent
        self.action_to_perform = action_to_perform

    def print_info(self):
        print("Agent {0} is walking toward agent {1}.".format(
            self.this_agent.name, self.other_agent.name))

class WaitForResponseState(AgentState):
    def __init__(self, other_agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_agent = other_agent
        self.counter = 1

    def print_info(self):
        print("Agent {0} is waiting for a response from agent {1}.".format(
            self.this_agent.name, self.other_agent.name))

class RandomWalkState(AgentState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def print_info(self):
        print("Agent {0} is walking around randomly.".format(
            self.this_agent.name))

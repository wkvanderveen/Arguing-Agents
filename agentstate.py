class AgentState(object):
    def __init__(self, this_agent, *args, **kwargs):
        self.this_agent = this_agent

class NegotiationState(AgentState):
    """docstring for NegotiationState"""
    def __init__(self, buy_or_sell, other_agent, duration=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buy_or_sell = buy_or_sell,
        self.other_agent = other_agent,
        self.duration = duration

    def print_info(self):
        print("Agent {0} is {1} agent {2} for {3} steps so far.".format(
            self.this_agent.name,
            ('selling to' if self.buy_or_sell[0] == 'sell' else 'buying from'),
            self.other_agent[0].name,
            self.duration))

class WalkToAgentState(AgentState):
    def __init__(self, other_agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_agent = other_agent

    def print_info(self):
        print("Agent {0} is walking toward agent {1}.".format(
            self.this_agent.name, self.other_agent.name))

class WaitForResponseState(AgentState):
    def __init__(self, other_agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.other_agent = other_agent
        self.counter = 2

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

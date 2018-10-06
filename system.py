"""docstring placeholder"""
from agent import *

class System():
    """docstring for System"""

    def __init__(self):
        self.time = 0
        self.agents = dict()

        print("System initialized.")

    def create_agent(self, name):
        """Create a new Agent in the system."""
        new_agent = Agent(name)
        self.agents[name] = new_agent

    def advance(self):
        """Advance the time by a value of 1."""

        print("\nUpdating system...\n{}\n".format('-' * 56))

        requests_sent = 0
        requests_received = 0

        responses_sent = 0
        responses_received = 0

        # Let all agents send their messages
        for name, agent in self.agents.items():
            requests_sent += agent.send_requests()
            responses_sent += agent.send_responses()

        # Let all agents receive messages
        for name, agent in self.agents.items():
            requests_received += agent.receive_requests()
            responses_received += agent.receive_responses()

        for name, agent in self.agents.items():
            if isinstance(agent.state, NegotiationState):
                # TODO: negotiate process
                agent.state.duration += 1


            elif isinstance(agent.state, RandomWalkState):
                agent.move_random()

            elif isinstance(agent.state, WalkToAgentState):
                # TODO: find best free move to this agent
                pass

        self.time += 1


    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))

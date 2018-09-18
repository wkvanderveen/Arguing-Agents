"""docstring placeholder"""

from agent.agent import Agent

class System():
    """docstring for System"""

    def __init__(self):
        self.time = 0
        self.agents = dict()

        print("System initialized.\n")

    def create_agent(self, name, beliefs, desires, intentions, goals):
        """Create a new Agent in the system."""
        new_agent = Agent(name,
                          beliefs,
                          desires,
                          intentions,
                          goals)
        self.agents[name] = new_agent

    def advance(self):
        """Advance the time by a value of 1."""

        messages_sent = 0
        messages_received = 0

        for name, agent in self.agents.items():
            messages_sent += agent.send_messages()

        for name, agent in self.agents.items():
            messages_received += agent.receive_messages()

        self.time += 1
        print("{}\nUpdating system...".format('-'*56))
        print("> Time is now {}".format(self.time))
        print("> Messages Sent: {0}, Messages Received: {1}\n".format(
            messages_sent, messages_received))

    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))

"""docstring placeholder"""

from agent import Agent

class System():
    """docstring for System"""
    def __init__(self):
        self.time = 0
        self.agents = dict()

        print("System initialized.\n")

    def create_agent(self, name, beliefs, desires, intentions, goals):
        """Create a new Agent in the system."""
        self.agents[name] = Agent(name,
                                  beliefs,
                                  desires,
                                  intentions,
                                  goals)

    def advance(self):
        """Advance the time by a value of 1."""
        self.time += 1
        message_store = []
        for name, agent in self.agents.items():
            message_store.extend(agent.send_message(name))
            agent.outgoing_messages = []
        for message in message_store:
            self.agents[message.recipient].receive_message(message)
        print("Updating system...")
        print("> Time is now {}".format(self.time))
        print("> Messages transferred: {}\n".format(len(message_store)))



    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.\n".format(
            self.time, len(self.agents)))

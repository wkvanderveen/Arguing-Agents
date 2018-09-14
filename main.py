"""Docstring for main.py"""

class Agent():
    """docstring for Agent"""
    def __init__(self, name, beliefs, desires, intentions, goals):
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions
        self.goals = goals
        self.outgoing_messages = []

    def print_info(self):
        """Print the relevant information about this agent."""
        print("This is Agent '{}'.".format(self.name))
        print("\tCurrent modal operators:")
        print("\t- Beliefs:\t{}".format(self.beliefs))
        print("\t- Desires:\t{}".format(self.desires))
        print("\t- Intentions:\t{}".format(self.intentions))
        print("\t- Goals:\t{}".format(self.goals))

    def send_message(self, recipient):
        """Send all messages in the outgoing message list."""
        for message in self.outgoing_messages:
            message.sender = self.name
            SYSTEM.agents['recipient'].receive_message(message)
        else:
            # After all messages are sent, empty the list of outgoing
            # messages.
            self.outgoing_messages = []


    def receive_message(self, message):
        """Parse and process incoming messages."""

        pass

class Message():
    """docstring for Message"""
    def __init__(self, time, message_type, sender, recipient):
        self.time = time
        self.message_type = message_type


class System():
    """docstring for System"""
    def __init__(self):
        self.time = 0
        self.agents = dict()

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

    def print_info(self):
        """Print the information about the system."""
        print("Time = {0}.\nNumber of agents = {1}.".format(
            self.time, len(self.agents)))

SYSTEM = System()

SYSTEM.create_agent("union",
                    [],
                    [],
                    [],
                    [(30, ("wage.increase", True)),
                     (None, ("unemployment", False))]
                   )

SYSTEM.create_agent("management",
                    [],
                    [],
                    [],
                    [(None, ("save", True))])


SYSTEM.advance()

SYSTEM.agents["union"].print_info()

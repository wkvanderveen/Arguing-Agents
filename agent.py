class Agent():
    """docstring for Agent"""
    def __init__(self, name, beliefs, desires, intentions, goals):
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions
        self.goals = goals
        self.outgoing_messages = []

        print("Agent '{}' initialized.\n".format(self.name))

    def print_info(self):
        """Print the relevant information about this agent."""
        print("This is Agent '{}'.".format(self.name))
        print("\tCurrent modal operators:")
        print("\t- Beliefs:\t{}".format(self.beliefs))
        print("\t- Desires:\t{}".format(self.desires))
        print("\t- Intentions:\t{}".format(self.intentions))
        print("\t- Goals:\t{}\n".format(self.goals))

    def send_message(self, recipient):
        """Send all messages in the outgoing message list."""
        for message in self.outgoing_messages:
            message.sender = self.name
            message.recipient = recipient
        return self.outgoing_messages

    def receive_message(self, message):
        """Parse and process incoming messages."""
        message.recipient = self.name
        print("Agent '{0}' has just received a {1}.\n".format(
            message.recipient, message.message_type))

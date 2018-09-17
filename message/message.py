"""docstring placeholder"""

class Message():
    """docstring for Message"""
    def __init__(
            self, time, message_type, sender="UNKNOWN", recipient="UNKNOWN"):

        self.time = time
        self.message_type = message_type
        self.sender = sender
        self.recipient = recipient

        print("Message ({}) initialized.\n".format(self.message_type))

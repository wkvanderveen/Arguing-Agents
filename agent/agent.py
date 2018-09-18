"""docstring placeholder"""
from message.message import *


class Agent():
    """docstring for Agent"""
    def __init__(self, name, beliefs, desires, intentions, goals):
        self.name = name
        self.beliefs = beliefs
        self.desires = desires
        self.intentions = intentions
        self.goals = goals
        self.outgoing_messages = []
        self.incoming_messages = []

        print("Agent '{}' initialized.\n".format(self.name))

    def print_info(self):
        """Print the relevant information about this agent."""
        print("This is Agent '{}'.".format(self.name))
        print("\tCurrent modal operators:")
        print("\t- Beliefs:\t{}".format(self.beliefs))
        print("\t- Desires:\t{}".format(self.desires))
        print("\t- Intentions:\t{}".format(self.intentions))
        print("\t- Goals:\t{}\n".format(self.goals))

    def generate_message(self, time, type_of_message, recipient,
            sentence, argument=None, response_msg_type='UNKNOWN'):

        if type_of_message == 'REQUEST':
            msg = RequestMessage(time=time,
                                 sender=self,
                                 recipient=recipient,
                                 sentence=sentence,
                                 argument=argument)
        elif type_of_message == 'RESPONSE':
            msg = ResponseMessage(time=time,
                                  sender=self,
                                  recipient=recipient,
                                  response_msg_type=response_msg_type,
                                  sentence=sentence,
                                  argument=argument)
        elif type_of_message == 'DECLARATION':
            msg = DeclarationMessage(time=time,
                                     sender=self,
                                     recipient=recipient,
                                     sentence=sentence)
        else:
            raise ValueError("Incorrect message type ({})".format(
                type_of_message))

        self.outgoing_messages.append(msg)

    def send_messages(self):
        messages_sent = 0

        for message in self.outgoing_messages:
            message.on_send()
            self.outgoing_messages.remove(message)
            message.recipient.incoming_messages.append(message)
            messages_sent += 1

        return messages_sent

    def receive_messages(self):
        messages_received = 0

        for message in self.incoming_messages:
            message.on_receive()
            self.incoming_messages.remove(message)
            messages_received += 1

        return messages_received

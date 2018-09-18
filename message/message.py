"""docstring placeholder"""
from abc import ABC, abstractmethod


class BaseMessage(ABC):
    """docstring for Message"""
    def __init__(self, time, sender=None, recipient=None):

        self.time = time
        self.sender = sender
        self.recipient = recipient
        """
        #TODO: Define type of the load (sentence or argument), when the difference in sentence and argument is clear.
        self.load = load # This defines load given with the message, can be None, sentence or an argument
        """

    @abstractmethod
    def on_receive(self):
        print("Message received")

    @abstractmethod
    def on_send(self):
        print("Message sent")


class RequestMessage(BaseMessage):
    def __init__(self, sentence, argument=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'REQUEST'
        self.sentence = sentence
        self.argument = argument

        print("Message ({}) initialized.\n".format(self.message_type))

    def on_send(self):
        print("Message of type {0} is sent at {1}".format(
            self.message_type, self.time))

    def on_receive(self):
        print("Message of type {0} is received at {1}\n".format(
            self.message_type, self.time))

    def convert_to_string(self):
        if self.argument == None:
            return "Request({0})".format(self.sentence.convert_to_string())
        else:
            return "Request({0}, {1})".format(self.sentence.convert_to_string(),
                                              self.argument.convert_to_string())


class ResponseMessage(BaseMessage):
    def __init__(self, sentence, argument=None,
            response_msg_type='UNKNOWN', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'RESPONSE'
        # Response Message Type can be of three types 1: ACCEPT, 2: REJECT 3: UNKNOWN
        self.response_msg_type = response_msg_type
        self.sentence = sentence
        self.argument = argument

        print("Message ({}) initialized.\n".format(self.message_type))

    def on_send(self):
        print("Message of type {0} is sent at {1}".format(
            self.message_type, self.time))

    def on_receive(self):
        print("Message of type {0} is received at {1}\n".format(
            self.message_type, self.time))

    def convert_to_string(self):
        if argument == None:
            if response_msg_type == 'ACCEPT':
                return "Accept({0})".format(self.sentence.convert_to_string())
            elif response_msg_type == 'REJECT':
                return "Reject({0})".format(self.sentence.convert_to_string())
            else:
                return "Response({0})".format(self.sentence.convert_to_string())
        else:
            if response_msg_type == 'ACCEPT':
                return "Accept({0}, {1})"\
                    .format(self.sentence.convert_to_string(),
                            self.argument.convert_to_string())
            elif response_msg_type == 'REJECT':
                return "Reject({0}, {1})"\
                    .format(self.sentence.convert_to_string(),
                            self.argument.convert_to_string())
            else:
                return "Response({0}, {1})"\
                    .format(self.sentence.convert_to_string(),
                            self.argument.convert_to_string())


class DeclarationMessage(BaseMessage):
    def __init__(self, sentence, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'DECLARATION'
        self.sentence = sentence

        print("Message ({}) initialized.\n".format(self.message_type))

    def on_send(self):
        print("Message of type {0} is sent at {1}".format(
            self.message_type, self.time))

    def on_receive(self):
        print("Message of type {0} is received at {1}\n".format(
            self.message_type, self.time))

    def convert_to_string(self, sentence, argument=None):
        return "Declaration({0})".format(sentence.convert_to_string())

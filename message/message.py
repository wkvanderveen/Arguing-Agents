"""docstring placeholder"""
from abc import ABC, abstractmethod


class BaseMessage(ABC):
    """docstring for Message"""
    def __init__(
            self,time, sender=None, recipient=None, load=None):
        self.time = time
        self.sender = sender
        self.recipient = recipient

        #TODO: Define type of the load (sentence or argument), when the difference in sentence and argument is clear.
        self.load = load # This defines load given with the message , can be None, sentence or an argument

    @abstractmethod
    def on_receive(self):
        print("Message received")

    @abstractmethod
    def on_send(self):
        print("Message sent")





class RequestMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'REQUEST'
        print("Message ({}) initialized.\n".format(self.message_type))

    def on_receive(self):
        print("Message of type {} is received at {} , Sent By: {}, Received By: {} ".format(self.message_type,
                                                                                            self.time,
                                                                                            self.sender.name,
                                                                                            self.recipient.name))

    def on_send(self):
        print("Message of type {} is sent at {} , Sent By: {}, Received By: {} ".format(self.message_type,
                                                                                        self.time,
                                                                                        self.sender.name,
                                                                                        self.recipient.name
                                                                                        ))





class ResponseMessage(BaseMessage):
    def __init__(self, response_msg_type = 'UNKNOWN', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'RESPONSE'
        self.response_msg_type=response_msg_type # Response Message Type can be of three types 1: ACCEPT, 2: REJECT 3: UNKNOWN
        print("Message ({}) initialized.\n".format(self.message_type))

    def on_receive(self):
        print("Message of type {} is received at {} , Sent By: {}, Received By: {}".format(self.message_type,
                                                                                           self.time,
                                                                                           self.sender.name,
                                                                                           self.recipient.name
                                                                                           ))

    def on_send(self):
        print("Message of type {} is sent at {} , Sent By: {}, Received By: {}".format(self.message_type,
                                                                                       self.time,
                                                                                       self.sender.name,
                                                                                       self.recipient.name
                                                                                       ))




class DeclarationMessage(BaseMessage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_type = 'DECLARATION'
        print("Message ({}) initialized.\n".format(self.message_type))


    def on_receive(self):
        print("Message of type {} is received at {} , Sent By: {}, Received By: {}".format(self.message_type,
                                                                                           self.time,
                                                                                           self.sender.name,
                                                                                           self.recipient.name
                                                                                           ))

    def on_send(self):
        print("Message of type {} is sent at {} , Sent By: {}, Received By: {}".format(self.message_type,
                                                                                       self.time,
                                                                                       self.sender.name,
                                                                                       self.recipient.name
                                                                                       ))

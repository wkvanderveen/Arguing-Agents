"""docstring placeholder"""
from abc import ABC, abstractmethod

from evaluation import BaseEvaluationProcess

from agentstate import NegotiationState, WalkToAgentState, RandomWalkState

class BaseMessage(ABC):
    """docstring for Message"""
    def __init__(self, sender=None, receiver=None):

        self.sender = sender
        self.receiver = receiver

class Response(BaseMessage):
    def __init__(self, response_type, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.response_type = response_type
        self.request = request

    def on_send(self):
        if self.response_type == 'no':
            print("{0} sends negative response to {1}.".format(
                self.sender.name, self.receiver.name))
        elif self.response_type == 'yes':
            print("{0} sends positive response to {1}.".format(
                self.sender.name, self.receiver.name))
        else:
            raise ValueError("Incorrect Response type sent: {}".format(
                self.response_type))

    def on_receive(self):
        if self.response_type == 'no':
            print("Negative response from {0} received by {1}.".format(
                self.sender.name, self.receiver.name))
        elif self.response_type == 'yes':
            print("Positive response from {0} received by {1}.".format(
                self.sender.name, self.receiver.name))

        else:
            raise ValueError("Incorrect Response type received: {}".format(
                self.response_type))


class Request(BaseMessage):
    def __init__(self, request_type, fruit, quantity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_type = request_type
        self.fruit = fruit
        self.quantity = quantity

    def on_send(self):
        print("{0} sent request to {1} {2} {3} {4} {5}".format(
            self.sender.name,
            self.request_type,
            self.quantity,
            self.fruit,
            'to' if self.request_type == 'sell' else 'from',
            self.receiver.name))

    def on_receive(self):
        print("{0} received request to {1} {2} {3} {4} {5}".format(
            self.receiver.name,
            'sell' if self.request_type == 'buy' else 'buy',
            self.quantity,
            self.fruit,
            'to' if self.request_type == 'buy' else 'from',
            self.sender.name))

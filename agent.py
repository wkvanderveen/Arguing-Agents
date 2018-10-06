"""docstring placeholder"""
from message import Request, Response
from agentstate import *
from grid import constants as gridconstants
from random import randint

class Agent():
    """docstring for Agent"""
    def __init__(self, name, position=[0,0], money=0):
        self.name = name
        self.position = position
        self.state = RandomWalkState(this_agent=self)
        self.money = money
        self.incoming_requests = []
        self.outgoing_requests = []
        self.incoming_responses = []
        self.outgoing_responses = []

        print("Agent '{}' initialized.".format(self.name))

    def print_info(self):
        """Print the relevant information about this agent."""
        print("This is Agent '{0}' on position {1}.".format(
          self.name,
          self.position))

    def move_random(self):
        while(True):
            choice = randint(1, 5)
            if choice == 1 and self.position[0] < gridconstants.TILES_X:
                self.position[0] += 1
                print("Randomly moved agent {0} to the right.".format(self.name))
                return
            elif choice == 2 and self.position[0] > 0:
                self.position[0] -= 1
                print("Randomly moved agent {0} to the left.".format(self.name))
                return
            elif choice == 3 and self.position[1] < gridconstants.TILES_Y:
                self.position[1] += 1
                print("Randomly moved agent {0} down.".format(self.name))
                return
            elif choice == 4 and self.position[1] > 0:
                self.position[1] -= 1
                print("Randomly moved agent {0} up.".format(self.name))
                return
            elif choice == 5:
                print("Randomly moved agent {0} nowhere.".format(self.name))
                return

    def generate_request(self, request_type, receiver, fruit, quantity):
        """Generate a buy or sell request for an adjacent agent."""
        msg = Request(sender=self,
                      request_type=request_type,
                      receiver=receiver,
                      fruit=fruit,
                      quantity=quantity)

        self.outgoing_requests.append(msg)


    def generate_response(self, response_type, receiver, request):
        """Generate an accept or reject response for a requesting agent."""
        msg = Response(sender=self,
                       response_type=response_type,
                       receiver=receiver,
                       request=request)

        self.outgoing_responses.append(msg)

    def send_requests(self):
        """Send all generated requests to the receivers."""
        requests_sent = 0

        for request in self.outgoing_requests:
            request.on_send()
            self.outgoing_requests.remove(request)
            if isinstance(request.receiver.state, NegotiationState):
                print("Request blocked -- agent already negotiating!")
            else:
                request.receiver.incoming_requests.append(request)
                requests_sent += 1
            self.state = WaitForResponseState(
                this_agent=self,
                other_agent=request.receiver)

        return requests_sent

    def receive_requests(self):
        """Receive requests from other agents."""
        requests_received = 0

        for request in self.incoming_requests:
            request.on_receive()

            self.incoming_requests.remove(request)
            requests_received += 1

            # TODO: Decision making process to generate response

            ### HARDCODE: ANSWER 'YES' TO REQUEST
            self.generate_response(response_type='yes',
                                   receiver=request.sender,
                                   request=request)
            ###

            # The agent shouldn't move away before answering the request
            self.state = WaitForResponseState(
                this_agent=self,
                other_agent=request.sender)

        return requests_received

    def send_responses(self):
        """Send all generated responses to the receivers."""
        responses_sent = 0

        for response in self.outgoing_responses:
            response.on_send()
            self.outgoing_responses.remove(response)
            response.receiver.incoming_responses.append(response)
            responses_sent += 1
            if response.response_type == 'yes':
                self.state = NegotiationState(this_agent=self,
                                              buy_or_sell=response.request.request_type,
                                              other_agent=response.sender)

        return responses_sent


    def receive_responses(self):
        """Receive responses from other agents."""
        responses_received = 0

        for response in self.incoming_responses:
            response.on_receive()
            self.incoming_responses.remove(response)
            responses_received += 1
            if response.response_type == 'yes':
                self.state = NegotiationState(this_agent=self,
                                              buy_or_sell=response.request.request_type,
                                              other_agent=response.sender)

        return responses_received

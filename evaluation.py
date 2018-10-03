''' This will define evaluation process of message '''
from wff import Wff


class BaseEvaluationProcess():

    @classmethod
    def evaluate(cls,message=None ,*args, **kwargs):
        if message:
            message_type = message.message_type
            print("Evaluating message {}", message_type)

            if message_type == 'REQUEST':
                cls.evaluate_request(message=message, *args, **kwargs)

            elif message_type == 'RESPONSE':
                cls.evaluate_response(message=message, *args, **kwargs)

            elif message_type == 'DECLARATION':
                cls.evaluate_declaration(message=message, *args, **kwargs)

            else:
                print(" Can not evaluate message!!")

        else:
            print("No Message for evaluation")


    @classmethod
    def evaluate_request(cls,message=None, *args, **kwargs):
        sentence=message.sentence
        argument=message.argument


        wff1= Wff(wff_type='implies',
                  wffs=[sentence,argument]
                  )
        wff2=Wff(wff_type='implies',
                  wffs=[argument,sentence]
                  )

        temp_bel_1=Wff(wff_type='bdig',
                        times=[0],
                        predicate=['Bel'],
                        agents=[message.recipient],
                        wffs=[wff1])
        temp_bel_2=Wff(wff_type='bdig',
                        times=[0],
                        predicate=['Bel'],
                        agents=[message.recipient],
                        wffs=[wff2])


        if temp_bel_1 in message.recipient.beliefs or temp_bel_2 in message.recipient.beliefs:
            #accept
            message.recipient.generate_message(0,'RESPONSE', message.sender,
            sentence, response_msg_type='ACCEPT')
        else:
            #reject
            message.recipient.generate_message(0, 'RESPONSE', message.sender,
                                               sentence, response_msg_type='REJECT')



    @classmethod
    def evaluate_response(cls,message=None, *args, **kwargs):
        sentence = message.sentence
        argument = message.argument
        if message.response_msg_type == 'ACCEPT':
            #print(sentence.convert_to_string().join('was Rejected'))
            #print("Rejected {}",sentence.predicate[1])
            print("Allowed to use printer")
        elif message.response_msg_type == 'REJECT':
            #print(message.sentence.action)
            #print("Rejected {}", sentence.predicate[1])
            print("Not allowed to use printer")

    @classmethod
    def evaluate_declaration(cls,message=None, *args, **kwargs):
        pass

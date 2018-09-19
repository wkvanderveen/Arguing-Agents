''' This will define evaluation process of message '''
from wff.wff import Wff


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
            pass
        else:
            #reject
            pass



    @classmethod
    def evaluate_response(cls,message=None, *args, **kwargs):
        sentence = message.sentence
        argument = message.argument
        if message.response_message_type == 'REJECT':
            #print(sentence.convert_to_string().join('was Rejected'))
            pass
        elif message.response_message_type == 'ACCEPT':
            #print(message.sentence.action)
            pass

    @classmethod
    def evaluate_declaration(cls,message=None, *args, **kwargs):
        pass
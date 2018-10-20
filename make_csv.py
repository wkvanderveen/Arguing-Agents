import pandas as pd


class MakeCsv():
    def make_csv(self):
        from main import SYSTEM

        all_agents=SYSTEM.get_all_agents_in_list()

        df = pd.DataFrame(columns=['elasticity',
                                   'paience',
                                   'money',
                                   'Total Negotiations',
                                   'Total Positive',
                                   'Total Negative',
                                   'Entities Value Start',
                                   'Entities Value End']
                          )
        i=0
        for agent in all_agents:
            negotiation_param=SYSTEM.get_negotiations_parameter_of_agent(agent.agent_id)
            entities_value_in_start=agent.cal_entities_value_in_start()

            entities_of_agent = agent.entities_info.items()
            total_quantity_price=0
            for entity_name,value in entities_of_agent:
                entity_info = agent.entities_info[entity_name]
                if entity_info['isInterested']:
                    gap=SYSTEM.get_entity_global_average_price(entity_name)
                    if gap is None:
                        gap= (entity_info['min_selling_price']
                              +entity_info['max_buying_price'])/2

                    total_quantity_price+=gap*entity_info['quantity']


            #elasticity,paience,money,total_negotiations,total_positive,total_negative,quantity value


            df.loc[i]=[agent.elasticity,
                      agent.patience,
                      agent.money,
                      negotiation_param[0],
                      negotiation_param[1],
                      negotiation_param[2],
                      entities_value_in_start,
                      total_quantity_price]

            i+=1


        print(df)
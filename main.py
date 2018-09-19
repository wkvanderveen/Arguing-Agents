"""Docstring for main.py"""

from system.system import System
from message.message import RequestMessage
from wff.wff import Wff
SYSTEM = System()



# Create agents 'Alice' and 'Bob'
SYSTEM.create_agent(name="Alice",
                    beliefs=[],
                    desires=[],
                    intentions=[],
                    goals=[])

SYSTEM.create_agent(name="Bob",
                    beliefs=[],
                    desires=[],
                    intentions=[],
                    goals=[])

alices_goal_friends = Wff(wff_type='predicate',
                          times=[0],
                          predicate=['Do', "be.friends"],
                          agents=[SYSTEM.agents["Bob"]],
                          )
alices_goal = Wff(wff_type='bdig',
                  times=[0],
                  predicate=['Goal'],
                  agents=[SYSTEM.agents["Alice"]],
                  wffs=[alices_goal_friends])

alices_belief_let_use_printer = Wff(wff_type='predicate',
                                    times=[0],
                                    predicate=['Do', "let.use.printer"],
                                    agents=[SYSTEM.agents["Alice"]])

alices_belief_implies = Wff(wff_type='implies',
                            wffs=[alices_belief_let_use_printer,
                                  alices_goal_friends])

alices_belief = Wff(wff_type='bdig',
                    times=[0],
                    predicate=['Bel'],
                    agents=[SYSTEM.agents["Alice"]],
                    wffs=[alices_belief_implies])


bobs_goal_use_printer = Wff(wff_type='predicate',
                            times=[0],
                            predicate=['Do', "use.printer"],
                            agents=[SYSTEM.agents["Bob"]])

bobs_goal = Wff(wff_type='bdig',
                times=[0],
                predicate=['Goal'],
                agents=[SYSTEM.agents["Bob"]],
                wffs=[bobs_goal_use_printer])

bobs_belief = Wff(wff_type='predicate',
                  times=[0],
                  predicate=['Capable', "let.use.printer"],
                  agents=[SYSTEM.agents["Alice"]])

bobs_intention_friends = Wff(wff_type='predicate',
                             times=[0],
                             predicate=['Do', "be.friends"],
                             agents=[SYSTEM.agents["Bob"]])

bobs_intention = Wff(wff_type='bdig',
                     times=[0],
                     predicate=['Int'],
                     agents=[SYSTEM.agents["Bob"]],
                     wffs=[bobs_intention_friends])

SYSTEM.agents["Alice"].beliefs.append(alices_belief)
SYSTEM.agents["Alice"].goals.append(alices_goal)


SYSTEM.agents["Bob"].beliefs.append(bobs_belief)
SYSTEM.agents["Bob"].goals.append(bobs_goal)
SYSTEM.agents["Bob"].intentions.append(bobs_intention)


SYSTEM.agents["Alice"].print_info()

SYSTEM.agents["Bob"].print_info()

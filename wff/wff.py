""" docstring placeholder """

class Wff():
    def __init__(self, wff_type=None, times=[], terms=[],
            predicate=[None, None], wffs=[], agents=[], bdig=None,
            preference=None, message=None, send_receive=None, *args,
            **kwargs):

        self.wff_type = wff_type
        self.times = times
        self.terms = terms
        self.predicate = predicate
        self.wffs = wffs
        self.agents = agents
        self.bdig = bdig
        self.preference = preference
        self.message = message
        self.send_receive = send_receive


    def convert_to_string(self, print_verbose=False):
        # Detect type of wff
        if self.wff_type == 'time_compare':
            return "{0} < {1}".format(self.times[0], self.times[1])

        if self.wff_type == 'term_compare':
            return "{0} = {1}".format(self.terms[0], self.terms[1])

        if self.wff_type == 'predicate':
            return "[{0}, {1}({2})]".format(self.times[0],
                                            self.predicate[0],
                                            ','.join(self.predicate[1]))

        if self.wff_type == 'not':
            return "!{0}".format(self.wffs[0].convert_to_string())

        if self.wff_type == 'and':
            return "{0} & {1}".format(self.wffs[0].convert_to_string(), self.wffs[1].convert_to_string())

        if self.wff_type == 'or':
            return "{0} | {1}".format(self.wffs[0].convert_to_string(), self.wffs[1].convert_to_string())

        if self.wff_type == 'implies':
            return "{0} -> {1}".format(self.wffs[0].convert_to_string(), self.wffs[1].convert_to_string())

        if self.wff_type == 'for all':
            return "FORALL {0} {1}".format(self.terms[0], self.wffs[0].convert_to_string())

        if self.wff_type == 'exists':
            return "EXISTS {0} {1}".format(self.terms[0], self.wffs[0].convert_to_string())

        if self.wff_type == 'with_message':
            return "[{0}, {1}({2}, {3}) {4}]"\
                .format(self.times[0], self.send_receive, self.agents[0].name,
                        self.agents[1].name, self.message.convert_to_string())

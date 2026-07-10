from qualify.woe import BusinessTypeWOE
import math

class Qualify:
    def __init__(self, example_data):
        good = example_data['good']
        bad = example_data['bad']
        types_sample_data = { 
            'good': [x.types for x in good],
            'bad': [x.types for x in bad]
        }
        self.woe = BusinessTypeWOE(types_sample_data) 

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def calc_woe(self, types): # todo
        score = 0
        for t in types:
            score += self.woe.get_weight(t)
        return score

    def calc_score(self, lead):
        type_woe = self.calc_woe(lead.types)

        score = self.sigmoid(type_woe)
        return score

    def qualify(self, leads, threshold = 0.6):
        qualified_leads = []
        unqualified_leads = []
        for lead in leads:
            score = self.calc_score(lead)
            if score > threshold:
                qualified_leads.append(lead)
            else:
                unqualified_leads.append(lead)

        return qualified_leads, unqualified_leads

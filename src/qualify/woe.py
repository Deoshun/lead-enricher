import math
from collections import Counter

class BusinessTypeWOE:
    def __init__(self, sample_data):
        self.dict = {}
        # We start with 1 (Laplace smoothing) to avoid log(0) or division by zero
        self.num_good = 1 
        self.num_bad = 1
        self.calibrate(sample_data)

    def calibrate(self, sample_data):
        """
        Phase 1: Count all occurrences to establish stable global totals.
        """
        # Reset storage
        counts = {} 

        # Process 'good' samples
        for types_list in sample_data.get('good', []):
            self.num_good += len(types_list)
            for t in types_list:
                if t not in counts:
                    counts[t] = {'good': 1, 'bad': 1} # Smoothing
                counts[t]['good'] += 1

        # Process 'bad' samples
        for types_list in sample_data.get('bad', []):
            self.num_bad += len(types_list)
            for t in types_list:
                if t not in counts:
                    counts[t] = {'good': 1, 'bad': 1} # Smoothing
                counts[t]['bad'] += 1

        """
        Phase 2: Calculate scores once based on the final totals.
        """
        for evidence, event_counts in counts.items():
            score = self.calc_evidence_score(event_counts)
            self.dict[evidence] = {
                'event_count': event_counts,
                'score': score
            }

    def calc_evidence_score(self, event_counts):
        # Using the stable totals established in Phase 1
        dist_good = event_counts['good'] / self.num_good
        dist_bad = event_counts['bad'] / self.num_bad
        return math.log(dist_good / dist_bad)

    def get_weight(self, evidence):
        data = self.dict.get(evidence)
        return data['score'] if data else 0

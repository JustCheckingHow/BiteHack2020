from so_parser import StackOverflowCarrers
import pandas as pd
from collections import defaultdict
import os 

class Aggregator:
    def __init__(self):
        self.src = 'data/stack_overflow_careers'
        self.SOC = StackOverflowCarrers(100)

    def build_statistics(self):
        filenames = [os.path.join(self.src, fn) for fn in os.listdir(self.src)]
        statistics = defaultdict(list)
        for filename in filenames:
            tags, desc = self.SOC.parse_job_posting(filename)
            if tags:
                statistics['tags'].append(tags)
                for k, v in desc.items():
                    statistics[k].append(v)

        df = pd.DataFrame.from_dict(statistics)
        df.to_csv('Example.csv')


if __name__ == '__main__':
    ag = Aggregator()
    ag.build_statistics()

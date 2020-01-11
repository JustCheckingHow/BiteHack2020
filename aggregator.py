from so_parser import StackOverflowCarrers
import pandas as pd
from collections import defaultdict
import os 

class Aggregator:
    def __init__(self):
        self.src = 'data/stack_overflow_careers'
        self.SOC = StackOverflowCarrers(100)
        # self.db = pd.read_csv('db.csv')

    def build_statistics(self):
        filenames = [os.path.join(self.src, fn) for fn in os.listdir(self.src)]
        statistics = defaultdict(list)
        for filename in filenames:
            try:
                tags, desc = self.SOC.parse_job_posting(filename)
                if tags:
                    statistics['Tags'].append(list(set(tags)))
                    if len(tags) > 20:
                        print(tags, desc)
                    for k, v in desc.items():
                        statistics[k].append(v)
            except Exception as e:
                print(f"Failed {filename}")
        df = pd.DataFrame.from_dict(statistics)
        df.to_csv('db.csv')

    def search_in_db(self, position):
        positions = self.db.loc[self.db['Role'] == position]

if __name__ == '__main__':
    ag = Aggregator()
    # ag.build_statistics()

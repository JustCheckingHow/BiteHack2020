from so_parser import StackOverflowCarrers
import pandas as pd
from collections import defaultdict, Counter
import os
import json
import ast
import numpy as np


class Aggregator:
    def __init__(self):
        self.src = '../data/stack_overflow_careers'
        self.SOC = StackOverflowCarrers(100)
        self.db = pd.read_pickle('db.pkl')
        self.unique_roles = self.db['Role'].unique()

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
        df = df.dropna(subset=['Role'])
        # parse string which encodes a list to an actual list
        # df['Skills'] = df['Tags'].apply(lambda x: np.array(ast.literal_eval(x))
                                        # )
        df.to_pickle('db.pkl')

    def search_in_db(self, role, limit=None):
        """
        Return statistics for a role from a db 
        """
        new_roles = self.db.loc[self.db['Role'].isin([role])]
        all_tags = new_roles['Tags'].to_numpy()
        # flatten all tags
        if all_tags.any():
            flat_tags = np.concatenate(all_tags).ravel()
            c = Counter(flat_tags)
            final_statistics = []
            for k, v in c.most_common(limit):
                final_statistics.append({
                    'skill': k,
                    'count': v,
                    'percentage': v * 100 / len(new_roles)
                })
            return json.dumps(final_statistics)
        else:
            return json.dumps("")


if __name__ == '__main__':
    ag = Aggregator()
    # ag.build_statistics()
    print(ag.search_in_db('Product Manager', 2))

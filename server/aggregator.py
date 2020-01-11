from so_parser import StackOverflowCarrers
import pandas as pd
from collections import defaultdict, Counter
import os
import json 

class Aggregator:
    def __init__(self):
        self.src = 'data/stack_overflow_careers'
        self.SOC = StackOverflowCarrers(100)
        self.db = pd.read_csv('db.csv')

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
        db = db.dropna(subset=['Role'])
        # parse string which encodes a list to an actual list
        db['Skills'] = db['tags'].apply(lambda x: np.array(ast.literal_eval(x))
                                        )
        df.to_csv('db.csv')

    def search_in_db(self, role):
        """
        Return statistics for a role from a db 
        """
        new_roles = self.db.loc[self.db['Role'].isin([role])]
        all_tags = new_roles['Skills'].to_numpy()
        # flatten all tags
        flat_tags = np.concatenate(all_tags).ravel()
        c = Counter(flat_tags)
        final_statistics = defaultdict(dict)
        for k, v in c.items():
            final_statistics[k] = {
                'count': v,
                'percentage': v * 100 / len(new_roles)
            }
        return json.dumps(final_statistics)


if __name__ == '__main__':
    ag = Aggregator()
    # ag.build_statistics()

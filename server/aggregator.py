from so_parser import StackOverflowCarrers
import pandas as pd
from collections import defaultdict, Counter
import os
import json
import ast
import numpy as np
import re

def term_in_doc(t, d):
    if t in d:
        return True
    else:
        return False
    
def calc_tfidf(t, d, D):
    """
    All specific role create a document    
    """
    freqs = [D[role][t] for role in D]
    tmax = max(freqs)
    tf = 0.5 + \
        0.5*d[t]/tmax
    x = [term_in_doc(t, D[role]) for role in D]
    idf = np.log(len(d)/sum(x))
    return tf*idf


class Aggregator:
    def __init__(self):
        self.src = '../data/soc'
        self.SOC = StackOverflowCarrers(100)
        self.db = pd.read_pickle('concat_db.pkl')
        self.unique_roles = self.db['Role'].unique()
        self.role_tfidf = self.create_documents_counts(self.db)

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
        df.to_pickle('db_large.pkl')

    def search_in_db(self, role, limit=None):
        """
        Return statistics for a role from a db 
        """
        new_roles = self.db.loc[self.db['Role'].str.contains(
            role, flags=re.IGNORECASE, regex=True)]
        all_tags = new_roles['Tags'].to_numpy()
        # flatten all tags
        if all_tags.any():
            flat_tags = np.concatenate(all_tags).ravel()
            c = Counter(flat_tags)
            final_statistics = []
            for k, v in c.most_common(limit):
                final_statistics.append({
                    'skill':
                    k,
                    'count':
                    v,
                    'percentage':
                    int(v * 100 / len(new_roles))
                })
            return json.dumps(final_statistics)
        else:
            return json.dumps("")

    def create_documents_counts(self, df):
        global_counts = Counter()
        role_counts = {}
        for role in df['Role'].unique():
            if not role: 
                continue
            skillset = df['Tags'].loc[df['Role'] == role].to_numpy()
            # flatten all tags
            flat_tags = np.concatenate(skillset).ravel()
            tcount = Counter(flat_tags)
            global_counts += tcount
            if role not in role_counts:
                role_counts[role] = Counter()
            role_counts[role] += tcount
            
        tfidf_role = {}
        for role in df['Role'].unique():
            if not role:
                continue
            tfidf_role[role] = Counter()
            skillset = df['Tags'].loc[df['Role'] == role].to_numpy()
            flat_tags = np.concatenate(skillset).ravel()
            # print(f"Role {role}")
            for skill in flat_tags:
                score = calc_tfidf(skill, role_counts[role], role_counts)
                # print(f"\t{skill}: {score}")
                tfidf_role[role][skill] = score
                
        return tfidf_role

if __name__ == '__main__':
    ag = Aggregator()
    # ag.build_statistics()
    print(ag.search_in_db('Data *', 10))

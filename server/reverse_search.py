import pandas as pd
import pickle
from collections import defaultdict


class ReverseSearch:
    def __init__(self):
        try:
            self.reverse_dict = pickle.load(open("reverse_dict.pkl", "rb"))
        except:
            self.prepare_db()
    
    def prepare_db(self):
        df = pickle.load(open("db.pkl", "rb"))
        reverse_dict = defaultdict(list)
        
        for _, row in df.iterrows():
            for tag in list(row['Tags']):
                reverse_dict[tag].append(row['Role'].replace("'", ""))
        
        for key in reverse_dict.keys():
            reverse_dict[key] = set(reverse_dict[key])

        pickle.dump(reverse_dict, open("reverse_dict.pkl", "wb"))

    def reverse_search(self, words, limit=None):
        data = []
        for word in words:
            data.extend(self.reverse_dict[word])

        counter = Counter(data)

        final_statistics = defaultdict(dict)
        for k, v in counter.most_common(limit):
            final_statistics[k] = {
            'count': v,
            'percentage': v * 100 / len(words)
        }
        return json.dumps(final_statistics)



if __name__ == "__main__":
    rs = ReverseSearch()
    rs.prepare_db()

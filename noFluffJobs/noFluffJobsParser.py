from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import os

class noFluffJobsParser():

    def __init__(self):
        self.results = []

        self.ens_data = {
            'Role': [],
            'Tags' : []
        }

    def parse_data(self, data):
        bs = BeautifulSoup(data, 'html.parser')
        role = bs.find('nfj-posting-header', {'id': 'posting-header'}).find('h1').getText()
        tags = []

        for aux in bs.findAll('nfj-posting-requirements'):
            for tag in aux.findAll('button'):
                tags += [tag.getText()]

        return role, tags

    def parse_files(self, filenames):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue

            with open(filename, 'r', encoding = 'utf-8') as f:
                data = f.read()
                role, tags = parser.parse_data(data)

                if tags:
                    self.ens_data['Role'] += [role]
                    self.ens_data['Tags'] += [tags]

if __name__ == '__main__':
    parser = noFluffJobsParser()

    ls = os.listdir('noFluffJobs/websites')

    parser.parse_files(['./noFluffJobs/websites/' + dir for dir in ls])

    print(parser.ens_data)

    df = pd.DataFrame.from_dict(parser.ens_data)

    df.to_csv('no_fluffs.csv')




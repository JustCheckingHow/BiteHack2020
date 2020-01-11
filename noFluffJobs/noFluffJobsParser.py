from bs4 import BeautifulSoup
import codecs
import os

ls = os.listdir()

with codecs.open("angular-developer-bravura-solutions-polska-warsaw-f7xjbfmb.html", 'r', encoding='iso-8859-15') as f:
    data = f.read()
bs = BeautifulSoup(data, "html.parser")
print(bs.find_all("dd"))


import pandas as pd
from collections import defaultdict

ens_data = {
    'Role': [],
    'Tags' : []
}
stoplist = ["\n", " "]

def parse(data):
    bs = BeautifulSoup(data, "html.parser")
    role = bs.find_all("h1")[1].text
#     role=""
    buttons = bs.find_all('button')[1:]
    tags = []
    for el in buttons:
        if el.text.find("+1") != -1:
            break
        tags += [el.text.lower().replace("\n", "")]

    return role, tags



for filename in ls:
    if not filename.endswith('.html'):
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        txt = f.read()
        r, t = parse(txt)
        if t:
            ens_data['Role'].append(r)
            ens_data['Tags'].append(t)

df = pd.DataFrame.from_dict(ens_data)

df.to_csv("no_fluffs.csv")

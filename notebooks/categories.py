from __future__ import print_function

import math
import os
from sets import Set
import numpy as np
import scipy.sparse as sps
from scipy import io
from sklearn.preprocessing import normalize
import pandas as pd


def load_data(folder):
    datasets = {}
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]
    for file_path in result:
        data_file = open(file_path)
        dat = data_file.read()
        lst = dat.splitlines()
        datasets[file_path[27:]] = lst
    return datasets


data = load_data('../jupyter-wikidata/matrix')
articles = data['po_slowach-categories-simple-20120104']
art_cats = {}
categories = set()
for article in articles:
    id_and_categories = article.split('\t')
    articleId = id_and_categories[0]
    del id_and_categories[0]
    cats = [int(x) for x in id_and_categories]
    art_cats[articleId] = cats
    new_cats = set(cats)
    categories |= new_cats

flatten = lambda l: [item for sublist in l for item in sublist]
flattenart_cats = flatten(art_cats.values())
hA = pd.Series(flattenart_cats).value_counts()
print(hA)

maxCategoryId = np.amax(list(categories)) + 1
hAnB = sps.dok_matrix((maxCategoryId, maxCategoryId))
for a in art_cats:
    for b in art_cats[a]:
        for c in art_cats[a]:
            hAnB[b, c] += 1
print(hAnB)

p = sps.dok_matrix((maxCategoryId, maxCategoryId))
for i in categories:
    cardinalityA = hA[i]
    for j in categories:
        cardinalityB = hA[j]
        print(i,j)
        p[i, j] = hAnB[i, j] / (cardinalityA + cardinalityB - hAnB[i, j])

CURRENT_DIR = os.path.dirname(__file__)
pMatrixPath = os.path.join(CURRENT_DIR, "pMatrix.mtx")
io.mmwrite(pMatrixPath, p)
del p

# copy this to another file...
p = io.mmread(pMatrixPath)
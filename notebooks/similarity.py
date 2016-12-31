from __future__ import print_function

import math
import os

import numpy as np
import scipy.sparse as sps
from scipy import io
from sklearn.preprocessing import normalize


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
print(data.keys())

tfidfVecs = data['po_slowach-lista-simple-20120104-sampled100']

articles = {}
exceptions = []
for rawTfidf in tfidfVecs:
    article = rawTfidf.split("#")
    tfidf = map(lambda x: x.split("-"), article[1].split(" "))
    if len(tfidf) > 1:
        try:
            articles[int(article[0])] = dict(tfidf)  # dla kazdego artykulu slownik id_slowa->waga
        except ValueError:
            exceptions.extend([int(article[0])])

print(exceptions)
print(len(exceptions))  # parsing problems... scientific notations sucks
print(len(articles))


def similarity(a, b):
    dot_product = 0.0
    magnitude1 = 0.0
    magnitude2 = 0.0

    for k in a:
        if k in b:
            dot_product += float(a[k]) * float(b[k])
            magnitude1 += float(a[k]) ** 2
            magnitude2 += float(b[k]) ** 2

    magnitude1 = math.sqrt(magnitude1)
    magnitude2 = math.sqrt(magnitude2)
    if (magnitude1 != 0.0) | (magnitude2 != 0.0):
        return dot_product / (magnitude1 * magnitude2)
    else:
        return 0.0


maxArticleId = np.amax(articles.keys()) + 1
distanceMatrix = sps.dok_matrix((maxArticleId, maxArticleId))
print(maxArticleId)

for k in articles:
    for j in articles:
        if (k > j):
            print(k, j)
            sim = 1 - similarity(articles[k], articles[j])
            distanceMatrix[k, j] = sim
            distanceMatrix[j, k] = sim

distanceMatrixNorm = normalize(distanceMatrix, norm='l1', axis=1)

print(distanceMatrix)
CURRENT_DIR = os.path.dirname(__file__)
distanceMatrixPath = os.path.join(CURRENT_DIR, "distanceMatrix.mtx")
distanceMatrixNormPath = os.path.join(CURRENT_DIR, "distanceMatrixNorm.mtx")
io.mmwrite(distanceMatrixPath, distanceMatrix)
io.mmwrite(distanceMatrixNormPath, distanceMatrixNorm)
del distanceMatrix
del distanceMatrixNorm

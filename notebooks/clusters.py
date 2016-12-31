from __future__ import print_function

import os

from scipy import io
from sklearn.cluster import DBSCAN

CURRENT_DIR = os.path.dirname(__file__)
distanceMatrixPath = os.path.join(CURRENT_DIR, "distanceMatrix.mtx")
distanceMatrixNormPath = os.path.join(CURRENT_DIR, "distanceMatrixNorm.mtx")
distanceMatrix = io.mmread(distanceMatrixPath)
distanceMatrixNorm = io.mmread(distanceMatrixNormPath)
print(distanceMatrix)
print(distanceMatrixNorm)

db = DBSCAN(eps=0.1, min_samples=3, metric='precomputed', leaf_size=5).fit(distanceMatrixNorm)
labels = db.labels_

print(labels)
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_clusters_)


def get_labels():
    raw_labels = map(lambda x: x.split("\t"), data['po_slowach-articles_dict-simple-20120104'])
    labels = dict(map(lambda (x, y): [y, x], raw_labels))
    return labels

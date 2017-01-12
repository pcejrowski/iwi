from __future__ import print_function

import math
import os

import numpy as np
import scipy.sparse as sps
from scipy import io
from sklearn.preprocessing import normalize
import utils

__outputFileName = "articlesSimiliarity.mtx"
__debug = False

def calculate(articleFeatures, recreate):
    if recreate or not utils.exists(__outputFileName):
        tfidfVecs = articleFeatures
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

        if __debug:
            print(exceptions)
            print(len(exceptions))  # parsing problems... scientific notation sucks
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
        similarityMatrix = sps.dok_matrix((maxArticleId, maxArticleId))
        if __debug:
            print(maxArticleId)

        for k in articles:
            for j in articles:
                if (k > j):
                    sim = similarity(articles[k], articles[j])
                    similarityMatrix[k, j] = sim
                    similarityMatrix[j, k] = sim

        similarityMatrixNorm = normalize(similarityMatrix, norm='l1', axis=1)
        utils.save(__outputFileName, similarityMatrixNorm)

    return __outputFileName

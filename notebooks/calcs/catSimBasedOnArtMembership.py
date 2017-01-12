import utils

import numpy as np
import scipy.sparse as sparse
import pandas as pd

from sklearn.preprocessing import normalize

__outputFileName = "catSimBasedOnArtMembership.mtx"
__debug = False

def calculate(art_cat_membership, recalculate):
    if recalculate or not utils.exists(__outputFileName):
        art_cats = {}
        categories = set()
        for article in art_cat_membership:
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
        if __debug:
            print(hA)

        maxCategoryId = np.amax(list(categories)) + 1
        hAnB = sparse.dok_matrix((maxCategoryId, maxCategoryId))
        for a in art_cats:
            for b in art_cats[a]:
                for c in art_cats[a]:
                    hAnB[b, c] += 1
        if __debug:
            print(hAnB)

        p = sparse.dok_matrix((maxCategoryId, maxCategoryId))
        for i in categories:
            cardinalityA = hA[i]
            for j in categories:
                cardinalityB = hA[j]
                if __debug:
                    print(i, j)
                p[i, j] = hAnB[i, j] / (cardinalityA + cardinalityB - hAnB[i, j])
        hAnBNormalized = normalize(hAnB)
        utils.save(__outputFileName, hAnBNormalized)
        del p

    return __outputFileName
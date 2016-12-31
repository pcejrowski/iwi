import utils

import numpy as np
import scipy.sparse as sps
import pandas as pd

__outputFileName = "catSimBasedOnArtSim.mtx"
__debug = False

def calculate(artSimilarity, artCatMembership, recalculate):
    if recalculate or not utils.exists(__outputFileName):
        artsByCat = articlesByCategories(artCatMembership)
        maxCategoryId = np.amax(list(artsByCat.keys())) + 1
        hAnB = sps.dok_matrix((maxCategoryId, maxCategoryId))
        artSimKeys = set([x for x, y in artSimilarity.todok().keys()])
        for cat1, arts1 in artsByCat.iteritems():
            for cat2, arts2 in artsByCat.iteritems():
                sum = 0
                count = 0
                for art1 in arts1:
                    for art2 in arts2:
                        if art1 in artSimKeys and art2 in artSimKeys:  # z powodu "glupiego" samplowania danych
                            sum += artSimilarity[art1, art2]
                            count += 1
                if count > 0: # z powodu "glupiego" samplowania danych
                    hAnB[cat1, cat2] = sum / count
        utils.save(__outputFileName, hAnB)
    return __outputFileName


def articlesByCategories(artCatMembership):
        categories_arts = dict()
        for article in artCatMembership:
            id_and_categories = article.split('\t')
            articleId = int(id_and_categories[0])
            del id_and_categories[0]
            cats = [int(x) for x in id_and_categories]
            for cat in cats:
                if categories_arts.has_key(cat):
                    categories_arts[cat].add(articleId)
                else:
                    categories_arts[cat] = {articleId}
        return categories_arts
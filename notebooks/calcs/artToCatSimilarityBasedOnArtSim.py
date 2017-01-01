import utils

import numpy as np
import scipy.sparse as sps
import pandas as pd
from sklearn.preprocessing import normalize

__outputFileName = "artToCatSimBasedOnArtSim.mtx"
__debug = False

def calculate(artSimilarity, artCatMembership, recalculate):
    if recalculate or not utils.exists(__outputFileName):
        artsByCat = articlesByCategories(artCatMembership)
        maxCategoryId = np.amax(list(artsByCat.keys())) + 1
        artToCatSim = sps.dok_matrix((maxCategoryId, maxCategoryId))
        artSimKeys = set([x for x, y in artSimilarity.todok().keys()])

        for art in artSimKeys:
            for cat, arts in artsByCat.iteritems():
                sum = 0
                count = 0
                for catArt in arts:
                    if catArt in artSimKeys:  # z powodu "glupiego" samplowania danych
                        sum += artSimilarity[art, catArt]
                        count += 1
                if count > 0: # z powodu "glupiego" samplowania danych
                    artToCatSim[art, cat] = sum / count
        utils.save(__outputFileName, artToCatSim)
    return __outputFileName


def articlesByCategories(artCatMembership): #TODO duplikacja
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
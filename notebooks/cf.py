from decimal import Decimal

import utils

import calcs.rating as rating
import pandas as pd

__outputFileName1 = "cf_article_based.csv"
__outputFileName2 = "cf_category_based.csv"


def articleBased(articlesSimilarity, artNamesDict, recalculate):
    if recalculate or not utils.exists(__outputFileName1):
        used = []
        unique = [x for x in articlesSimilarity.indices if x not in used and (used.append(x) or True)]
        indexes = [artNamesDict.get(elem) for elem in unique]
        data_neighbours = pd.DataFrame(index=indexes, columns=range(1, 11))
        for i in unique:
            row = articlesSimilarity.getrow(i)
            neighbours = list(reversed(rating.sort_coo(row.tocoo())))[:10]
            data_neighbours.ix[artNamesDict.get(i), :10] = map(lambda z: artNamesDict.get(z[1]), neighbours)
        data_neighbours.to_csv(utils.createPath(__outputFileName1), sep=',', encoding='utf-8')
    return __outputFileName1


def getScore(history, similarities):
    return sum(history * similarities) / sum(similarities)


def categoryBased(artBasedSim, assignements, artCatSim, artNamesDict, catNamesDict, recalculate):
    if recalculate or not utils.exists(__outputFileName2):
        artIndexDict = {v: k for k, v in artNamesDict.iteritems()}
        # fixme: refactor the following lines
        art_cats = {}
        categories = set()
        for article in assignements:
            id_and_categories = article.split('\t')
            article_id = id_and_categories[0]
            del id_and_categories[0]
            cats = [int(x) for x in id_and_categories]
            art_cats[article_id] = cats
            new_cats = set(cats)
            categories |= new_cats

        cats = [catNamesDict.get(elem) for elem in categories]
        used = []
        indexes = [x for x in cats if x not in used and (used.append(x) or True)]
        art_cat_sim = artCatSim.todok()
        scores = {}
        for article, cats in art_cats.iteritems():
            try:
                art_name = artNamesDict.get(int(article))
                similar_articles = artBasedSim.loc[art_name]
                for similar in similar_articles:
                    for cat in cats:
                        score = art_cat_sim[artIndexDict.get(similar), cat]
                        if cat in scores:
                            scores[cat].append((similar, score))
                        else:
                            scores[cat] = []
            except (TypeError, KeyError):
                pass
        recommendations = pd.DataFrame(index=indexes, columns=range(1, 7))
        for cat, score in scores.iteritems():
            sorted_scores = map(lambda i: i[0], list(reversed(sorted(score, key=lambda i: i[1]))))[:6]
            recommendations.ix[catNamesDict.get(cat), :6] = sorted_scores
        recommendations = recommendations.dropna(how='all')

        recommendations.to_csv(utils.createPath(__outputFileName2), sep=',', encoding='utf-8')
    return __outputFileName2

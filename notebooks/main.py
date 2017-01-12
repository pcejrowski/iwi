import utils

import calcs.catSimBasedOnArtMembership
import calcs.artSimBasedOnFeatures
import calcs.catSimBasedOnArtSim
import calcs.artToCatSimilarityBasedOnArtSim
from scipy.sparse import coo_matrix, find
import sys

from itertools import izip


recreate = False

data = utils.load_data("../jupyter-wikidata/matrix/sample")
print("data files: " + str(data.keys()))

print("Calculating categorySimilarityBasedOnMembership") # Cat x Cat matrix
membershipData = data['po_slowach-categories-simple-20120104']
categorySimilarityBasedOnMembership_filename = calcs.catSimBasedOnArtMembership.calculate(membershipData, recreate)

print("Calculating articlesSimilarity") # Art x Art matrix
articlesFeatures = data['po_slowach-lista-simple-20120104']
articlesSimilarity_filename = calcs.artSimBasedOnFeatures.calculate(articlesFeatures, recreate)
articlesSimilarity = utils.read(articlesSimilarity_filename)

print("Calculating categorySimilarityBasedOnArticlesSimilarity") # Cat x Cat matrix
categorySimilarityBasedOnArticlesSimilarity_filename = calcs.catSimBasedOnArtSim.calculate(articlesSimilarity, membershipData, recreate)

print("Calculating articlesToCategorySimilarityOnArticlesSimilarity") # Art x Cat matrix
articlesToCategorySimilarityOnArticlesSimilarity_filename = calcs.artToCatSimilarityBasedOnArtSim.calculate(articlesSimilarity, membershipData, recreate)


simMembership = utils.read(categorySimilarityBasedOnMembership_filename)
simArtSim = utils.read(categorySimilarityBasedOnArticlesSimilarity_filename)
artCatSim = utils.read(articlesToCategorySimilarityOnArticlesSimilarity_filename)

#===============================================================
simCat = simMembership + simArtSim
artSuperSim = artCatSim * simCat
#===============================================================

countBefore1 = artSuperSim.count_nonzero()
for article in membershipData:
    id_and_categories = article.split('\t')
    articleId = int(id_and_categories[0])
    del id_and_categories[0]
    cats = [int(x) for x in id_and_categories]
    for cat in cats:
        artSuperSim[articleId, cat] = 0

artSuperSim.eliminate_zeros()
countAfter1 = artSuperSim.count_nonzero()
print('removed=' + str(countAfter1 - countBefore1) + ' and left=' + str(countAfter1))

def sort_coo(m):
    tuples = izip(m.row, m.col, m.data)
    return sorted(tuples, key=lambda x: (x[2]))

sorted = sort_coo(artSuperSim.tocoo())
top = sorted[-len(sorted)/10:]

raw_art_labels = map(lambda x: x.split(), data['po_slowach-articles_dict-simple-20120104'])
art_labels = dict(map(lambda (x, y): [y, x], raw_art_labels))

raw_cat_labels = map(lambda x: x.split(), data['po_slowach-cats_dict-simple-20120104'])
cat_labels = dict(map(lambda (x, y): [y, x], raw_cat_labels))

from sets import Set
x = Set()
y = Set()
for t in top:
    x.add(str(t[1]))
    y.add(str(t[0]))

for t in top:
    if t[1] != 18941 and t[1] < 13983:
        try:
            print(art_labels[str(t[0])] + ' - ' + cat_labels[str(t[1])])
        except:
            sys.stdout.write('.')

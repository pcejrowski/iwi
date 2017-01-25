import utils

import calcs.catSimBasedOnArtMembership
import calcs.artSimBasedOnFeatures
import calcs.catSimBasedOnArtSim
import calcs.artToCatSimilarityBasedOnArtSim
import calcs.metrics as metrics
import calcs.rating as rating
from scipy.sparse import coo_matrix, find
import sys
import pandas as pd
import cf
recreate = False

data = utils.load_data("../jupyter-wikidata/matrix/sample")
print("data files: " + str(data.keys()))

raw_art_labels = map(lambda x: x.split(), data['po_slowach-articles_dict-simple-20120104'])
artNamesDict = dict(map(lambda (x, y): [int(y), x], raw_art_labels))

raw_cat_labels = map(lambda x: x.split(), data['po_slowach-cats_dict-simple-20120104'])
catNamesDict = dict(map(lambda (x, y): [int(y), x], raw_cat_labels))


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

catToCatSim_Membership = utils.read(categorySimilarityBasedOnMembership_filename)
catToCatSim_ArtsSim = utils.read(categorySimilarityBasedOnArticlesSimilarity_filename)
artToCatSim_ArtsSim = utils.read(articlesToCategorySimilarityOnArticlesSimilarity_filename)

print("Collaborative filtering approaches")
print("Article based top 10 suggestions of neighbours per article")
artBasedCF_filename = cf.articleBased(articlesSimilarity, artNamesDict, recreate)
artBasedCF = pd.DataFrame.from_csv(utils.createPath(artBasedCF_filename))
print("Category based")
# different similarite measure might be used as 1st argument
catBasedCF_filename = cf.categoryBased(artBasedCF, membershipData, artToCatSim_ArtsSim, artNamesDict, catNamesDict, recreate)
catBasedCF = pd.read_csv(utils.createPath(catBasedCF_filename))
print(catBasedCF)

print("Rating basic similarity")
artToCatSim_Basic = artToCatSim_ArtsSim
rating.rate(artToCatSim_Basic, "Basic", membershipData, None, artNamesDict, catNamesDict)

print("Rating membership similarity")
artToCatSim_X_CatMembershipSim = artToCatSim_Basic * catToCatSim_Membership
rating.rate(artToCatSim_X_CatMembershipSim, "Membership", membershipData, None, artNamesDict, catNamesDict)
del artToCatSim_X_CatMembershipSim

print("Rating artsim similarity")
artToCatSim_X_CatArtSim = artToCatSim_Basic * catToCatSim_ArtsSim
rating.rate(artToCatSim_X_CatArtSim, "CatArtSim", membershipData, None, artNamesDict, catNamesDict)
del artToCatSim_X_CatArtSim

print("Rating combined similarity")
artToCatSim_X_CatCombinedSim = artToCatSim_Basic * (catToCatSim_Membership + catToCatSim_ArtsSim)
rating.rate(artToCatSim_X_CatCombinedSim, "Combined", membershipData, None, artNamesDict, catNamesDict)
del artToCatSim_X_CatCombinedSim
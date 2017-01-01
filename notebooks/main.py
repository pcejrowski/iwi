import utils

import calcs.catSimBasedOnArtMembership
import calcs.artSimBasedOnFeatures
import calcs.catSimBasedOnArtSim
import calcs.artToCatSimilarityBasedOnArtSim



recreate = False

data = utils.load_data("jupyter-wikidata/matrix/sample")
print("data files: " + str(data.keys()))

print("Calculating categorySimilarityBasedOnMembership") # Cat x Cat matrix
membershipData = data['po_slowach-categories-simple-20120104']
categorySimilarityBasedOnMembership_filename = calcs.catSimBasedOnArtMembership.calculate(membershipData, recreate)
# print(utils.read(categorySimilarityBasedOnMembership_filename))

print("Calculating articlesSimilarity") # Art x Art matrix
articlesFeatures = data['po_slowach-lista-simple-20120104']
articlesSimilarity_filename = calcs.artSimBasedOnFeatures.calculate(articlesFeatures, recreate)
articlesSimilarity = utils.read(articlesSimilarity_filename)

print("Calculating categorySimilarityBasedOnArticlesSimilarity") # Cat x Cat matrix
categorySimilarityBasedOnArticlesSimilarity_filename = calcs.catSimBasedOnArtSim.calculate(articlesSimilarity, membershipData, recreate)

print("Calculating articlesToCategorySimilarityOnArticlesSimilarity") # Art x Cat matrix
articlesToCategorySimilarityOnArticlesSimilarity_filename = calcs.artToCatSimilarityBasedOnArtSim.calculate(articlesSimilarity, membershipData, recreate)



import utils

import calcs.catSimBasedOnArtMembership
import calcs.artSimBasedOnFeatures
import calcs.catSimBasedOnArtSim



recreate = False

data = utils.load_data("jupyter-wikidata/matrix/sample")
print("data files: " + str(data.keys()))

print("Calculating categorySimilarityBasedOnMembership")
membershipData = data['po_slowach-categories-simple-20120104']
categorySimilarityBasedOnMembership_filename = calcs.catSimBasedOnArtMembership.calculate(membershipData, recreate)
# print(utils.read(categorySimilarityBasedOnMembership_filename))

print("Calculating articlesSimilarity")
articlesFeatures = data['po_slowach-lista-simple-20120104']
articlesSimilarity_filename = calcs.artSimBasedOnFeatures.calculate(articlesFeatures, recreate)
articlesSimilarity = utils.read(articlesSimilarity_filename)

print("Calculating categorySimilarityBasedOnArticlesSimilarity")
categorySimilarityBasedOnArticlesSimilarity_filename = calcs.catSimBasedOnArtSim.calculate(articlesSimilarity, membershipData, recreate)

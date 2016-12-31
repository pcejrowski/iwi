import utils

import calcs.catSimBasedOnMembership
import calcs.artSimBasedOnFeatures



recreate = False

data = utils.load_data("jupyter-wikidata/matrix/sample")
print("data files: " + str(data.keys()))

membershipData = data['po_slowach-categories-simple-20120104']
categorySimilarityBasedOnMembership_filename = calcs.catSimBasedOnMembership.calculate(membershipData, recreate)
print(categorySimilarityBasedOnMembership_filename)
# print(utils.read(categorySimilarityBasedOnMembership_filename))

articlesFeatures = data['po_slowach-lista-simple-20120104']
articlesSimilarity_filename = calcs.artSimBasedOnFeatures.calculate(articlesFeatures, recreate)
print(articlesSimilarity_filename)
# print(utils.read(articlesSimilarity_filename))

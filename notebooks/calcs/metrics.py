
import numpy
import os

def numberOfChildParentConnections(artToCatTopSims, categoryTree):
    return 0


CURRENT_DIR = os.path.dirname(__file__)

def getSamplePath(label):
    FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "manual-rating")
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    return os.path.join(FILES_DIR, label)


def generateSampleForManualRating(artToCatTopSims, artNamesDict, catNamesDict, label):
    samplePath = getSamplePath(label)

    # numOfSamples = 100
    # numToSkip = int(len(artToCatTopSims)/numOfSamples)
    # if not os.path.exists(samplePath):
    #     with open(samplePath, 'a') as the_file:
    #         for idx, x in enumerate(artToCatTopSims):
    #             if(idx % numToSkip == 0):
    #                 the_file.write("{}->{}:0\n".format(artNamesDict.get(x[0], x[0]), catNamesDict.get(x[1], x[1])))
    numOfSamples = 100
    if not os.path.exists(samplePath):
        with open(samplePath, 'a') as the_file:
            for idx, x in enumerate(artToCatTopSims[:numOfSamples]):
                the_file.write("{}->{}:0\n".format(artNamesDict.get(x[0], x[0]), catNamesDict.get(x[1], x[1])))


def fromManualRating(label):
    samplePath = getSamplePath(label)
    metricSum = 0
    with open(samplePath, 'r') as the_file:
        lines = the_file.readlines()
        for line in lines:
            metricSum += int(line.split(":")[1])

    return float(metricSum)/len(lines)


def numberOfExistingConnections(artToCatSim, artCatMembership):
    countBefore1 = artToCatSim.count_nonzero()
    numOfExisitingFound = 0
    numOfExisiting = 0
    for article in artCatMembership:
        id_and_categories = article.split('\t')
        articleId = int(id_and_categories[0])
        del id_and_categories[0]
        cats = [int(x) for x in id_and_categories]
        for cat in cats:
            numOfExisiting +=1
            if(artToCatSim[articleId, cat] != 0):
                numOfExisitingFound += 1

        # artToCatSim.eliminate_zeros()
    countAfter1 = countBefore1 - numOfExisiting
    return (1-float(countAfter1)/countBefore1, float(numOfExisitingFound)/numOfExisiting)


def variance(artToCatSim):
    return numpy.var(artToCatSim.data)
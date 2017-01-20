
import metrics

def rate(artToCatSim, label, membershipData, categoryTree, artNamesDict, catNamesDict):
    # countBefore1 = artToCatSim.count_nonzero()
    # for article in membershipData:
    #     id_and_categories = article.split('\t')
    #     articleId = int(id_and_categories[0])
    #     del id_and_categories[0]
    #     cats = [int(x) for x in id_and_categories]
    #     for cat in cats:
    #         artToCatSim[articleId, cat] = 0
    #
    #     artToCatSim.eliminate_zeros()
    # countAfter1 = artToCatSim.count_nonzero()
    # print('removed=' + str(countAfter1 - countBefore1) + ' and left=' + str(countAfter1))

    # raw_art_labels = map(lambda x: x.split(), data['po_slowach-articles_dict-simple-20120104'])
    # art_labels = dict(map(lambda (x, y): [y, x], raw_art_labels))
    #
    # raw_cat_labels = map(lambda x: x.split(), data['po_slowach-cats_dict-simple-20120104'])
    # cat_labels = dict(map(lambda (x, y): [y, x], raw_cat_labels))

    # from sets import Set
    # x = Set()
    # y = Set()
    #
    #
    # for t in topConnections:
    #     x.add(str(t[1]))
    #     y.add(str(t[0]))
    #
    # for t in topConnections:
    #     if t[1] != 18941 and t[1] < 13983:
    #         try:
    #             print(art_labels[str(t[0])] + ' - ' + cat_labels[str(t[1])])
    #         except:
    #             sys.stdout.write('.')


    topConnections = getTopConnections(artToCatSim)

    metrics.generateSampleForManualRating(topConnections, artNamesDict, catNamesDict, label)
    manualMetric = metrics.fromManualRating(label)
    print("Manual: {}".format(manualMetric))
    childParentMetric = metrics.numberOfChildParentConnections(topConnections, categoryTree)
    print("ChildParent: {}".format(childParentMetric))
    exisitingConnsMetric = metrics.numberOfExistingConnections(artToCatSim, membershipData)
    print("ExisitngConns: {}".format(exisitingConnsMetric))
    variance = metrics.variance(artToCatSim)
    print("Variance: {}".format(variance))


def getTopConnections(artToCatSim, number = None):
    sorted = sort_coo(artToCatSim.tocoo())
    if not number:
        number = len(sorted)/10
    top = sorted[-number:]
    return top


def sort_coo(m):
    from itertools import izip
    tuples = izip(m.row, m.col, m.data)
    return sorted(tuples, key=lambda x: (x[2]))
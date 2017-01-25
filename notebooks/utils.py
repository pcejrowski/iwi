import os
import scipy.io
import numpy as np
from scipy.sparse import coo_matrix

CURRENT_DIR = os.path.dirname(__file__)
FILES_DIR = os.path.join(CURRENT_DIR, "data")


def load_data(folder):
    datasets = {}
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]
    for file_path in result:
        data_file = open(file_path)
        dat = data_file.read()
        lst = dat.splitlines()
        datasets[file_path[len(folder) + 1:]] = lst
    return datasets


def createPath(filename):
    return os.path.join(FILES_DIR, filename)


def save(filename, data):
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    scipy.io.mmwrite(createPath(filename), data)


def read(filename):
    return scipy.io.mmread(createPath(filename)).tocsc()


def exists(filename):
    return os.path.exists(createPath(filename))


import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix


def plot_coo_matrix(m):
    if not isinstance(m, coo_matrix):
        m = coo_matrix(m)
    fig = plt.figure()
    ax = fig.add_subplot(111, axisbg='white')
    ax.plot(m.col, m.row, 's', color='black', ms=1)
    ax.set_xlim(0, m.shape[1])
    ax.set_ylim(0, m.shape[0])
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.figure.show()
    return

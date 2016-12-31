import os
import scipy.io

CURRENT_DIR = os.path.dirname(__file__)
FILES_DIR = os.path.join(CURRENT_DIR, "data")

def load_data(folder):
    datasets = {}
    result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(folder) for f in filenames]
    for file_path in result:
        data_file = open(file_path)
        dat = data_file.read()
        lst = dat.splitlines()
        datasets[file_path[len(folder)+1:]] = lst
    return datasets


def __createPath(filename):
    return os.path.join(FILES_DIR, filename)


def save(filename, data):
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)
    scipy.io.mmwrite(__createPath(filename), data)


def read(filename):
    return scipy.io.mmread(__createPath(filename)).tocsc()


def exists(filename):
    return os.path.exists(__createPath(filename))
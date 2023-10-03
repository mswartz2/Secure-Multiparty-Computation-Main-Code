import pickle
import os
import bz2
import sys

sys.path.append(os.getcwd())
# from main_folder.ecgPreprocessedData import Data


def write_to_pickle_file(data, filename):
    # make directory two levels higher
    if not os.path.exists(os.path.dirname(os.path.dirname(filename))):
        os.makedirs(os.path.dirname(os.path.dirname(filename)))

    # make directory one level higher
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    pickle_file = bz2.BZ2File(filename, "wb")
    pickle.dump(data, pickle_file)
    pickle_file.close()


def read_in_pickle_file(filename):
    with bz2.BZ2File(filename, "rb") as myfile:
        data_loaded = pickle.load(myfile)

    return data_loaded

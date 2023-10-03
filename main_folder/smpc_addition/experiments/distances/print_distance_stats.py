import os
import sys
import time
import numpy as np

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.distances.BoxPlotMaker import BoxPlotMaker
from main_folder.smpc_addition.experiments.distances.NormalizedGraphMaker import (
    NormalizedGraphMaker,
)
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)


def calc_simple_stats(arr, title):
    mean = np.mean(arr)
    max = np.max(arr)
    min = np.min(arr)
    median = np.median(arr)

    print(f"{title}\n\tmean:{mean:.3}, max:{max:.3}, min:{min:.3}, median:{median:.3}")


save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results\\"
norm_to_af_file = save_data_folder + "norm_to_af_distances.pickle"
af_to_norm_file = save_data_folder + "af_to_norm_distances.pickle"
normalized_file = save_data_folder + "other\\2017_normalized_distances.pickle_6"

# load distances
af_distances = read_in_pickle_file(af_to_norm_file)
norm_distances = read_in_pickle_file(norm_to_af_file)
normalized_distances = read_in_pickle_file(normalized_file)

boxPlotMaker = BoxPlotMaker()

os.chdir(save_data_folder)

boxPlotMaker.compare_absolute_differences(norm_distances, af_distances)

calc_simple_stats(normalized_distances, "Normalized Differences")

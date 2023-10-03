import os
import sys
import time

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.distances.BoxPlotMaker import BoxPlotMaker
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)

save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results\\"
norm_to_af_file = save_data_folder + "norm_to_af_distances.pickle"
af_to_norm_file = save_data_folder + "af_to_norm_distances.pickle"

# load distances
af_distances = read_in_pickle_file(af_to_norm_file)
norm_distances = read_in_pickle_file(norm_to_af_file)

boxPlotMaker = BoxPlotMaker()

os.chdir(save_data_folder)

boxPlotMaker.make_all_box_plots(9, "AF Dataset", norm_distances, af_distances)

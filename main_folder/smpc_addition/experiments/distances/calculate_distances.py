import os
import sys
import time

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.distances.BoxPlotMaker import BoxPlotMaker
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)

# load af dataset
complete_data_set = read_in_pickle_file(
    "main_folder\\ecgPreprocessedData\\Data\\CompleteDataSetFeatures.pickle"
)

X_class_norm = []
X_class_af = []
y_class_norm = []
y_class_af = []

# separate classes
for i in range(len(complete_data_set.labels)):
    if complete_data_set.labels[i] == 0:  # norm
        X_class_norm.append(complete_data_set.data[i])
        y_class_norm.append(0)
    else:  # af
        X_class_af.append(complete_data_set.data[i])
        y_class_af.append(1)

save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results\\"
file1 = save_data_folder + "norm_to_af_distances.pickle"
file2 = save_data_folder + "af_to_norm_distances.pickle"

write_to_pickle_file([4, 5, 6, 7], file1)
write_to_pickle_file([2.4, 4.5], file2)


boxPlotMaker = BoxPlotMaker()

os.chdir(
    "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\"
)

norm_to_af_distances = boxPlotMaker._get_distance_for_box_plot(
    X_class_norm, X_class_af, 9
)
af_to_norm_distances = boxPlotMaker._get_distance_for_box_plot(
    X_class_af, X_class_norm, 9
)

save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results\\"
file1 = save_data_folder + "norm_to_af_distances.pickle"
file2 = save_data_folder + "af_to_norm_distances.pickle"

write_to_pickle_file(norm_to_af_distances, file1)
write_to_pickle_file(af_to_norm_distances, file2)

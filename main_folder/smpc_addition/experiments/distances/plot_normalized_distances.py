import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.distances.NormalizedGraphMaker import (
    NormalizedGraphMaker,
)
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
X_class_all = []
y_class_all = []

# separate classes
for i in range(len(complete_data_set.labels)):
    if complete_data_set.labels[i] == 0:  # norm
        X_class_norm.append(complete_data_set.data[i])
        y_class_norm.append(0)
        y_class_all.append(0)
    else:  # af
        X_class_af.append(complete_data_set.data[i])
        y_class_af.append(1)
        y_class_all.append(1)
    X_class_all.append(complete_data_set.data[i])


normalizedGraphMaker = NormalizedGraphMaker()

save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results\\"

os.chdir(save_data_folder)


save_file = save_data_folder + "2017_normalized_distances.pickle"

for i in range(20):
    normalized_distances = normalizedGraphMaker.makeNormalizedGraph(
        X_class_all[0],
        X_class_all[1:],
        y_class_all[1:],
        f"normalized_{i}",
    )
    write_to_pickle_file(normalized_distances, f"{save_file}_{i}")

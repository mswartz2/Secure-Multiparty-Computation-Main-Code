import os
import sys
import time

sys.path.append(os.getcwd())
from distance_graphs.BoxPlotMaker import BoxPlotMaker
from ecgPreprocessedData.PickleFileUtils import read_in_pickle_file

# load af dataset
complete_data_set = read_in_pickle_file(
    "ecgPreprocessedData\\Data\\CompleteDataSetFeatures.pickle"
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


boxPlotMaker = BoxPlotMaker()

os.chdir(
    "c:\\Users\\swart\\Desktop\\secure-mpc-main\\distance_graphs\\box_plots\\box_plots_af"
)

t0 = time.time()
boxPlotMaker.make_all_box_plots(X_class_norm, X_class_af, 9, "AF Dataset")
t1 = time.time()
total_time_1 = t1 - t0

print(f"Total execution time NOT multithreaded: {total_time_1}")

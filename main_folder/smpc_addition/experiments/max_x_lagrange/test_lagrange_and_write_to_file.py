import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.max_x_lagrange.ExponentialGrapher import (
    ExponentialGrapher,
)
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)

# load af dataset
complete_data_set = read_in_pickle_file(
    "main_folder\\smpc_addition\\Data\\CompleteDataSetFeatures.pickle"
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


exponentialGrapher = ExponentialGrapher()

lagrange_maxes = []
x_points_to_label = []

for i in range(2, 8):
    first_x = 10**i
    second_x = first_x // 4
    third_x = first_x // 2
    fourth_x = second_x * 3
    lagrange_maxes.append([second_x, third_x, fourth_x, first_x])
    x_points_to_label.append(first_x)

# flatten list
lagrange_maxes = [item for sublist in lagrange_maxes for item in sublist]
# lagrange_maxes = [100, 1000, 10000, 100000, 1000000]
# x_points_to_label = [100, 1000, 10000,100000, 1000000]


os.chdir(
    "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances"
)
save_data_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\distances\\results"
results_file_name = save_data_folder + "exponential_data.pickle"

results = exponentialGrapher.makeGraph(
    X_class_all[0],
    X_class_all[1:],
    y_class_all[1:],
    lagrange_maxes,
    "2017Dataset-AllPoints",
    x_points_to_label,
    results_file_name,
    load_from_file=False,
)

write_to_pickle_file(results, results_file_name)

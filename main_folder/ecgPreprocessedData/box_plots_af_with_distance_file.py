import os
import sys
import time

sys.path.append(os.getcwd())
from distance_graphs.BoxPlotMaker import BoxPlotMaker
from ecgPreprocessedData.PickleFileUtils import read_in_pickle_file

# load distances
# af_distances = read_in_pickle_file(
#     "distance_graphs\\box_plots\\box_plots_af\\af_to_norm_distances.pickle"
# )
# norm_distances = read_in_pickle_file(
#     "distance_graphs\\box_plots\\box_plots_af\\norm_to_af_distances.pickle"
# )


af_distances = read_in_pickle_file(
    "distance_graphs\\box_plots\\box_plots_af\\1degree2shares\\af_to_norm_distances.pickle"
)
norm_distances = read_in_pickle_file(
    "distance_graphs\\box_plots\\box_plots_af\\1degree2shares\\norm_to_af_distances.pickle"
)

boxPlotMaker = BoxPlotMaker()

os.chdir(
    "c:\\Users\\swart\\Desktop\\secure-mpc-main\\distance_graphs\\box_plots\\box_plots_af\\1degree2shares"
)

# t0 = time.time()
boxPlotMaker.make_all_box_plots(9, "AF Dataset", norm_distances, af_distances)
# t1 = time.time()
# total_time_1 = t1 - t0


# print(f"Total execution time for AF dataset boxplots: {total_time_1}")


# boxPlotMaker.compare_absolute_differences(norm_distances, af_distances)

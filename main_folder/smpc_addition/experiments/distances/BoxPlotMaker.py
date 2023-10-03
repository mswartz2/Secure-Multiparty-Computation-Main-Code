from os import chdir, getcwd
import sys
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread


sys.path.append(getcwd())
from main_folder.smpc_addition.experiments.distances.DistanceCalculator import (
    DistanceCalculator,
)


class BoxPlotMaker(DistanceCalculator):
    def _get_neighbors_sum(self, arr, num_neighbors):
        arr = list(arr)
        arr.sort()
        neighbors = list()
        for i in range(num_neighbors):
            neighbors.append(arr[i])
        avg_distance = np.mean(neighbors)
        return avg_distance

    def _get_avg_distance_arr_between_points(
        self, arr1, arr2, num_neighbors, centralized_bool
    ):
        distances_all = []
        pseudo_y_arr = [1 for x in range(len(arr2))]

        i = 0
        for test_point in arr1:
            distances = []
            # if i == 0:
            #     print(i)
            print(i)
            i += 1
            if centralized_bool:
                distances = self._get_distances_one_to_many_normal(test_point, arr2)
            else:
                distances = self._get_distances_one_to_many_secure(
                    test_point, arr2, pseudo_y_arr, 100000
                )
            avg_dist = self._get_neighbors_sum(distances, num_neighbors)
            distances_all.append(avg_dist)
        return distances_all

    def _get_distance_for_box_plot(self, arr1, arr2, num_neighbors):
        avg_dists_to_self_norm = self._get_avg_distance_arr_between_points(
            arr1, arr1, num_neighbors, centralized_bool=True
        )

        avg_dists_to_self_secure = self._get_avg_distance_arr_between_points(
            arr1, arr1, num_neighbors, centralized_bool=False
        )

        avg_dists_to_arr2_norm = self._get_avg_distance_arr_between_points(
            arr1, arr2, num_neighbors, centralized_bool=True
        )

        avg_dists_to_arr2_secure = self._get_avg_distance_arr_between_points(
            arr1, arr2, num_neighbors, centralized_bool=False
        )

        return [
            avg_dists_to_self_norm,
            avg_dists_to_self_secure,
            avg_dists_to_arr2_norm,
            avg_dists_to_arr2_secure,
        ]

    def _one_box_plot(
        self,
        num_neighbors,
        x_labels,
        distances_arr,
        save_fig_path="",
    ):

        data = distances_arr

        fig, ax = plt.subplots()

        # build a box plot, don't show outliers
        ax.boxplot(data, showfliers=False)

        # axis labels
        ax.set_ylabel(f"Average Euclidean Distance with {num_neighbors} Neighbors")
        xticklabels = x_labels
        ax.set_xticklabels(xticklabels)

        # add horizontal grid lines
        ax.yaxis.grid(True)

        # show the plot
        # plt.show()
        if save_fig_path != "":
            plt.savefig(save_fig_path)
        else:
            plt.show()

    def make_all_box_plots(
        self,
        num_neighbors,
        dataset_name,
        norm_distances,
        af_distances,
    ):
        normal_point_x_labels = [
            "N-N: Traditional",
            "N-N: Secure",
            "N-AF: Traditional",
            "N-AF: Secure",
        ]
        af_point_x_labels = [
            "AF-AF: Traditional",
            "AF-AF: Secure",
            "AF-N: Traditional",
            "AF-N: Secure",
        ]

        # norm point box plot
        self._one_box_plot(
            num_neighbors,
            normal_point_x_labels,
            norm_distances,
            save_fig_path=f"{dataset_name}_normal_point_box_plot",
        )

        # af point box plot
        self._one_box_plot(
            num_neighbors,
            af_point_x_labels,
            af_distances,
            save_fig_path=f"{dataset_name}_af_point_box_plot",
        )

    def calc_absolute_diffs(self, arrs):
        arr1 = arrs[0]
        arr2 = arrs[1]

        diffs = []
        for x1, x2 in zip(arr1, arr2):
            diff = abs(x1 - x2)
            diffs.append(diff)

        return diffs

    def calc_stats_for_diffs(self, arrs, title):
        diffs = self.calc_absolute_diffs(arrs)
        diffs = np.array(diffs)
        mean = np.mean(diffs)
        max = np.max(diffs)
        min = np.min(diffs)
        median = np.median(diffs)

        print(
            f"{title}\n\tmean:{mean:.3}, max:{max:.3}, min:{min:.3}, median:{median:.3}"
        )

    def compare_absolute_differences(
        self,
        norm_distances,
        af_distances,
    ):

        n_n_arr = norm_distances[:2]
        n_af_arr = norm_distances[2:]
        af_af_arr = af_distances[:2]
        af_n_arr = af_distances[2:]

        self.calc_stats_for_diffs(n_n_arr, "N-N")
        self.calc_stats_for_diffs(n_af_arr, "N-AF")
        self.calc_stats_for_diffs(af_af_arr, "AF-AF")
        self.calc_stats_for_diffs(af_n_arr, "AF-N")

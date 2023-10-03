import numpy as np
import matplotlib.pyplot as plt

import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.experiments.distances.DistanceCalculator import (
    DistanceCalculator,
)
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)


class ExponentialGrapher(DistanceCalculator):
    def exponentialGraph(
        self,
        test_row,
        point_arr_x,
        point_arr_y,
        lagrange_arr,
        x_points_to_label,
        save_fig_path="",
        results_file_path="",
        load_from_file=True,
        saved_results=[],
    ):
        results = []
        if load_from_file == False:
            count = 0
            for x in lagrange_arr:
                print(f"On x_val: {x}")
                norm_dists = np.array(
                    self._get_distances_one_to_many_normal(test_row, point_arr_x)
                )
                secure_dists = np.array(
                    self._get_distances_one_to_many_secure(
                        test_row, point_arr_x, point_arr_y, x
                    )
                )

                sum_of_squared_differences = np.sum(
                    np.square(norm_dists - secure_dists)
                )
                results.append(sum_of_squared_differences)
            write_to_pickle_file(results, results_file_path)
        else:
            results = saved_results

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.scatter(lagrange_arr, results, color="royalblue")

        ax.set_ylabel("Sum of Squared Differences")
        ax.set_xlabel("Max X-Coordinate")

        ax.set_xscale("log")

        for i in range(len(lagrange_arr)):
            x_point = lagrange_arr[i]
            if x_point in x_points_to_label:
                text_str = f"y: {results[i]:.3}"
                # ax.annotate(text_str, (x_point, results[i] + 100))

        # Label every 4th point
        n = 4
        x = lagrange_arr
        y = results
        for i in range(n - 1, len(x), n):
            if i == len(x) - 1:
                ax.annotate(
                    f"{y[i]:.0f}",
                    xy=(x[i], y[i]),
                    xytext=(-40, -15),
                    textcoords="offset points",
                    va="center",
                )
            else:
                ax.annotate(
                    f"{y[i]:.3}",
                    xy=(x[i], y[i]),
                    xytext=(-5, 15),
                    textcoords="offset points",
                    va="center",
                )

        ax.scatter(x[n - 1 :: n], y[n - 1 :: n], color="orange")

        if save_fig_path != "":
            plt.savefig(save_fig_path)
        else:
            plt.show()

        return results

    def makeGraph(
        self,
        test_point,
        X_class,
        y_class,
        lagrange_arr,
        dataset_name,
        x_points_to_label,
        results_file_path="",
        load_from_file=True,
        saved_results=[],
    ):

        file_name = f"exponential_{dataset_name}"

        results = self.exponentialGraph(
            test_point,
            X_class,
            y_class,
            lagrange_arr,
            x_points_to_label,
            results_file_path=results_file_path,
            load_from_file=load_from_file,
            saved_results=saved_results,
        )
        return results

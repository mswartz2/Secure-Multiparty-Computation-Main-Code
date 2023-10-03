import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

from os import getcwd
import sys

sys.path.append(getcwd())
from main_folder.smpc_addition.experiments.distances.DistanceCalculator import (
    DistanceCalculator,
)

class NormalizedGraphMaker(DistanceCalculator):
    def graphNormlizedDifferences(
        self,
        test_point,
        X_class,
        y_class,
        dataset_name,
        max_x_lagrange=100000,
        save_fig_path="",
    ):

        norm_dists = self._get_distances_one_to_many_normal(test_point, X_class)
        secure_dists = self._get_distances_one_to_many_secure(
            test_point, X_class, y_class, max_x_lagrange
        )

        differences = []
        for x1, x2 in zip(norm_dists, secure_dists):
            diff = x1 - x2
            differences.append(abs(diff))

        normalized_differences = normalize([differences]).flatten()

        N = len(X_class)
        ind = np.arange(N)
        width = 0.35

        fig = plt.figure()
        ax = fig.add_subplot(111)

        # diffRects = ax.bar(ind, normalized_differences, width, color="royalblue")

        ax.scatter(ind, normalized_differences)

        ax.set_ylabel("Difference of Normalized Euclidean Distances")
        ax.set_xlabel("Sample number")

        y_ticks = np.arange(0, max(normalized_differences), 0.02)
        # ax.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.1])
        ax.set_yticks(y_ticks)
        ax.set_ylim(0, max(normalized_differences))

        if save_fig_path != "":
            plt.savefig(save_fig_path)
        else:
            plt.show()

        return normalized_differences



    def makeNormalizedGraph(
        self, test_point, X_class, y_class, dataset_name, max_x_lagrange=100000
    ):

        save_file = f"NormalizedDifferences_{dataset_name}"
        normalized_dists = self.graphNormlizedDifferences(
            test_point, X_class, y_class, dataset_name, max_x_lagrange, save_file
        )
        return normalized_dists

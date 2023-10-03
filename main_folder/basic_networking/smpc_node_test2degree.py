from scipy.interpolate import lagrange
from basic_networking.RandPoly import RandPoly


class SmpcNode:
    def __init__(self) -> None:
        pass

    def generate_functions(self, features_arr):
        all_functions = []
        for feature in range(len(features_arr)):
            func = RandPoly(name=f"f{feature}", n=2).poly
            all_functions.append(func)
        return all_functions

    def generate_shares_for_x_value(self, func_array, x):
        shares = []
        for func in func_array:
            shares.append(func(x))
        return shares

    def _get_feature_distances(self, arr1, arr2):
        distances = []
        for feature_a, feature_b in zip(arr1, arr2):
            dist = (feature_a - feature_b) ** 2
            distances.append(dist)
        return distances

    def _sum_distances(self, arr):
        return sum(arr)

    def _reconstruct(self, shares, xvals):
        x = xvals
        y = shares
        f = lagrange(x, y)
        return f(0)

    def calc_s_n_arr(self, g_n_arr, f_n):
        distances_arr = []
        s_1_arr = []
        for g_n in g_n_arr:
            distances_arr.append(self._get_feature_distances(g_n, f_n))

        for distances_1 in distances_arr:
            s_1 = self._sum_distances(distances_1)
            s_1_arr.append(s_1)

        return s_1_arr

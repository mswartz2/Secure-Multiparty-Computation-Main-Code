from os import chdir, getcwd
import sys

sys.path.append(getcwd())
from main_folder.smpc_addition.network_nodes.ClientSmpcAddition import (
    ClientSmpcAddition,
)
from main_folder.smpc_addition.network_nodes.ServerSmpcAddition import (
    ServerSmpcAddition,
)
from math import sqrt


class DistanceCalculator:
    # get list of euclidean distances normal
    def _euclidean_distance_normal(self, row1, row2):
        distance = 0.0
        for i in range(len(row1)):
            distance += (row1[i] - row2[i]) ** 2
        return sqrt(distance)

    def _get_distances_one_to_many_normal(self, test_point, point_arr):
        distances = []
        for point in point_arr:
            dist = self._euclidean_distance_normal(test_point, point)
            distances.append(dist)
        return distances

    def _get_distances_one_to_many_secure(
        self, test_point, point_arr_x, point_arr_y, max_x_lagrange=100000
    ):
        client = ClientSmpcAddition()
        server = ServerSmpcAddition()

        server.set_records_labels(point_arr_x, point_arr_y)
        f_shares_server, x_points = client.setup(test_point, rand_range=max_x_lagrange)

        (
            g_shares_client_all_records,
            h_shares_client_all_records,
            s_shares_server_all_records,
            labels,
        ) = server.get_values_for_client(x_points, f_shares_server)

        client._distance_computation(
            g_shares_client_all_records,
            h_shares_client_all_records,
            s_shares_server_all_records,
        )

        return client.distances

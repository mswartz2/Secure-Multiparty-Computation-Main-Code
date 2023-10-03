import numpy as np
from scipy.interpolate import lagrange
import socket
import json
import threading
from smpc_node import SmpcNode
from server import Server
import random

BYTE_SIZE = 1024


class Client(SmpcNode):
    def __init__(self) -> None:
        super().__init__()

    def get_distances_and_labels(self, test_row, serverNode: Server, num_points_for_lagrange):
        polynomials = self.generate_functions(test_row)

        # pick random points
        ids = random.sample(range(1, 500), num_points_for_lagrange)

        # generate shares
        shares = []
        for i in range(num_points_for_lagrange):
            share = self.generate_shares_for_x_value(polynomials, ids[i])
            shares.append[share]

        # send all ids and all shares except the last one to the server

        # receive array g_1, s_2, s_3, label from server for all server points
        g_1_arr, s_points_arr, label_arr = serverNode.get_gn_sn_for_client(
            ids, shares[:-1]
        )

        # calculate s_1_arr
        s_1_arr = self.calc_s_n_arr(g_1_arr, shares[-1])

        # calculate s_0_arr
        distance_labels_arr = []
        for s_1, s_2, s_3, label in zip(s_1_arr, s_2_arr, s_3_arr, label_arr):
            s_points = 
            s_0 = self._reconstruct([s_1, s_2, s_3])
            distance = np.sqrt(s_0)
            distance_labels_arr.append((distance, label))

        return distance_labels_arr

    def _get_neighbors(self, test_row, num_neighbors, serverNode: Server):
        distances = self.get_distances_and_labels(test_row, serverNode)
        distances.sort(key=lambda tup: tup[0])
        neighbors = list()
        for i in range(num_neighbors):
            neighbors.append([distances[i][0], distances[i][1]])
        return neighbors

    def predict_classification(self, test_row, num_neighbors, serverNode: Server):
        neighbors = self._get_neighbors(test_row, num_neighbors, serverNode)
        output_values = [row[-1] for row in neighbors]
        prediction = max(set(output_values), key=output_values.count)
        return prediction

    # def __init__(self, ip=socket.gethostname(), port=9999, name=""):
    #     self.name = name
    #     self.port = port
    #     self.ip = ip
    #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # def send(self, data):
    #     self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.client_socket.connect((self.ip, self.port))

    #     try:
    #         self.client_socket.sendall(bytes(data.encode("utf-8")))
    #         payload = self.client_socket.recv(BYTE_SIZE)

    #         decode = payload.decode("utf-8")
    #         msg = str(decode)

    #     finally:
    #         # self.client_socket.close()
    #         pass

    #     # self.client_socket.close()

    #     return msg

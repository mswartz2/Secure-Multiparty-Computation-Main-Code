import numpy as np
import random
from basic_networking.smpc_node_test2degree import SmpcNode
from basic_networking.server_test2degree import Server

class Client(SmpcNode):
    def __init__(self) -> None:
        super().__init__()

    def get_distances_and_labels(
        self, test_row, serverNode: Server, rand_range, rand_seed=4
    ):
        np.seterr(all="raise")

        polynomials = self.generate_functions(test_row)

        # pick 3 random points
        id_1, id_2, id_3 = random.Random(rand_seed).sample(range(1, rand_range), 3)

        # print(f"ids: {id_1, id_2, id_3}")

        # generate shares
        f_1 = self.generate_shares_for_x_value(polynomials, id_1)
        f_2 = self.generate_shares_for_x_value(polynomials, id_2)
        f_3 = self.generate_shares_for_x_value(polynomials, id_3)

        # send id_1, id_2, id_3, f_2, f_3 to server

        # receive array g_1, s_2, s_3, label from server for all server points
        g_1_arr, s_2_arr, s_3_arr, label_arr = serverNode.get_gn_sn_for_client(
            id_1, id_2, id_3, f_2, f_3
        )

        # calculate s_1_arr
        s_1_arr = self.calc_s_n_arr(g_1_arr, f_1)

        # calculate s_0_arr
        distance_labels_arr = []
        for s_1, s_2, s_3, label in zip(s_1_arr, s_2_arr, s_3_arr, label_arr):
            s_0 = self._reconstruct([s_1, s_2, s_3], [id_1, id_2, id_3])
            # print(f"S(0):{s_0}\t{s_1,s_2,s_3}")
            try:
                distance = abs(np.sqrt(s_0))
            except:
                # print(f"S(0):{s_0}\t{s_1,s_2,s_3}")
                distance = 0

            distance_labels_arr.append((distance, label))

        return distance_labels_arr

    def _get_neighbors(
        self,
        test_row,
        num_neighbors,
        serverNode: Server,
        rand_range,
        rand_seed=4,
    ):
        distances = self.get_distances_and_labels(
            test_row, serverNode, rand_range, rand_seed
        )
        distances.sort(key=lambda tup: tup[0])
        neighbors = list()
        for i in range(num_neighbors):
            neighbors.append([distances[i][0], distances[i][1]])
        return neighbors

    def predict_classification(
        self,
        test_row,
        num_neighbors,
        serverNode: Server,
        rand_range,
        rand_seed=4,
    ):
        neighbors = self._get_neighbors(
            test_row, num_neighbors, serverNode, rand_range, rand_seed
        )
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

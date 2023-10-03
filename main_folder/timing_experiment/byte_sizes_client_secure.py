import socket
import json
import time
import numpy as np

from PickleFileUtils import read_in_pickle_file
from network_nodes import ClientSecure


def run_trial_centralized(id, data_point):
    client = ClientSecure()
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))

    client.setup(data_point)
    # send data
    json_to_send = {
        "x_points": client.x_points,
        "f_2_share": client.f_values[1],
        "f_3_share": client.f_values[2],
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))
    client_msg_len = len(bytes(json.dumps(json_to_send), "UTF-8"))

    results = ""

    while True:
        received_from_server = clientsocket.recv(1024)
        if not received_from_server:
            break
        results += received_from_server.decode("UTF-8")

    results = json.loads(results)
    server_msg_len = len(bytes(json.dumps(results), "UTF-8"))

    clientsocket.close()

    return client_msg_len, server_msg_len


# load in dataset
complete_data_set = read_in_pickle_file("CompleteDataSetFeatures.pickle")
data_point = complete_data_set.data[0]

results_client_msg = []
results_server_msg = []

for i in range(1000):
    print("On rec ", i)
    client_msg_len, server_msg_len = run_trial_centralized(i, data_point)
    results_client_msg.append(client_msg_len)
    results_server_msg.append(server_msg_len)

print("\nSecure Method - Bytes per message")
print("Client to Server Message")
print(
    f"\fMin: {min(results_client_msg)}, Mean: {np.mean(results_client_msg)}, Max: {max(results_client_msg)}"
)
print("Server to Client Message")
print(
    f"\fMin: {min(results_server_msg)}, Mean: {np.mean(results_server_msg)}, Max: {max(results_server_msg)}\n"
)

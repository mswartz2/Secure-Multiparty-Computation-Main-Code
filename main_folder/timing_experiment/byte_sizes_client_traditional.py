import socket
import json
import time
import numpy as np

from PickleFileUtils import read_in_pickle_file


def run_trial_centralized(id, data_point):
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))
    # send data
    json_to_send = {
        "data": data_point,
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))
    client_msg_len = len(bytes(json.dumps(json_to_send), "UTF-8"))

    server_response = json.loads(clientsocket.recv(1024).decode("UTF-8"))
    server_msg_len = len(bytes(json.dumps(server_response), "UTF-8"))

    clientsocket.close()

    return client_msg_len, server_msg_len


# load in dataset
complete_data_set = read_in_pickle_file("CompleteDataSetFeatures.pickle")
data_point = complete_data_set.data[0]

results_client_msg = []
results_server_msg = []

for i in range(1000):
    client_msg_len, server_msg_len = run_trial_centralized(i, data_point)
    results_client_msg.append(client_msg_len)
    results_server_msg.append(server_msg_len)

print("\nTraditional Method - Bytes per message")
print("Client to Server Message")
print(
    f"\tMin: {min(results_client_msg)}, Mean: {np.mean(results_client_msg)}, Max: {max(results_client_msg)}"
)
print("Server to Client Message")
print(
    f"\tMin: {min(results_server_msg)}, Mean: {np.mean(results_server_msg)}, Max: {max(results_server_msg)}\n"
)

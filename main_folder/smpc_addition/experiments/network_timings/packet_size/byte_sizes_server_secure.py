import socket
import json
import time
import numpy as np

import sys
import os

sys.path.append(os.getcwd())
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)

from main_folder.smpc_addition.network_nodes.ServerSmpcAddition import (
    ServerSmpcAddition,
)

num_neighbors = 9

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()

port = 9999

# bind the socket to a public host, and a well-known port
serversocket.bind((host, port))

# become a server socket
serversocket.listen(5)

# load in dataset
complete_data_set = read_in_pickle_file(
    "main_folder\\smpc_addition\\Data\\CompleteDataSetFeatures.pickle"
)
# get labels
labels = complete_data_set.labels
# get data
data = complete_data_set.data

X_class = np.array(data)
y_class = np.array(labels)

# set up model
server_model = ServerSmpcAddition()
server_model.set_records_labels(X_class, y_class)

while True:
    # establish a connection
    print(f"\nListening on port {port}")
    clientsocket, addr = serversocket.accept()

    server_received_connection_time = time.time()
    json_data_received = json.loads(clientsocket.recv(1024).decode("UTF-8"))

    computation_start_time = time.time()

    x_points = json_data_received["x_points"]
    f_shares_server = json_data_received["f_shares_server"]

    (
        g_shares_client_all_records,
        h_shares_client_all_records,
        s_shares_server_all_records,
        labels,
    ) = server_model.get_values_for_client(x_points, f_shares_server)

    computation_end_time = time.time()

    json_data_to_send = {
        "g_shares_client_all_records": g_shares_client_all_records,
        "h_shares_client_all_records": h_shares_client_all_records,
        "s_shares_server_all_records": s_shares_server_all_records,
        "labels": labels.tolist(),
    }

    clientsocket.sendall(bytes(json.dumps(json_data_to_send), "UTF-8"))

    # close the client connection
    clientsocket.close()

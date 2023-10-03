import socket
import json
import time
from PickleFileUtils import read_in_pickle_file
import numpy as np
from sklearn.utils import shuffle
from network_nodes import ServerSecure

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
complete_data_set = read_in_pickle_file("CompleteDataSetFeatures.pickle")

data, labels = shuffle(
    complete_data_set.data, complete_data_set.labels, random_state=87
)
X_class = np.array(data)
y_class = np.array(labels)

# set up model
server_model = ServerSecure()
server_model.set_features_labels(X_class, y_class)

while True:
    # establish a connection
    print(f"\nListening on port {port}")
    clientsocket, addr = serversocket.accept()

    server_received_connection_time = time.time()
    json_data_received = json.loads(clientsocket.recv(1024).decode("UTF-8"))

    computation_start_time = time.time()

    x_points = json_data_received["x_points"]
    f_2_share = json_data_received["f_2_share"]
    f_3_share = json_data_received["f_3_share"]
    g_1_arr, s_2_arr, s_3_arr, labels = server_model.get_gn_sn_for_client(
        x_points, f_2_share, f_3_share
    )

    computation_end_time = time.time()

    json_data_to_send = {
        "g_1_arr": g_1_arr,
        "s_2_arr": s_2_arr,
        "s_3_arr": s_3_arr,
        "labels": labels.tolist(),
    }

    clientsocket.sendall(bytes(json.dumps(json_data_to_send), "UTF-8"))

    # close the client connection
    clientsocket.close()

import socket
import json
import numpy as np

import sys
import os

sys.path.append(os.getcwd())
from main_folder.smpc_addition.network_nodes.ServerTraditional import ServerTraditional
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
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
server_model = ServerTraditional()
server_model.set_up_model(X_class, y_class, num_neighbors)

while True:
    # establish a connection
    print(f"\nListening on port {port}")
    clientsocket, addr = serversocket.accept()

    json_data_received = json.loads(clientsocket.recv(1024).decode("UTF-8"))

    prediction = int(
        server_model.test_point(json_data_received["data"])
    )  # returns int32, but that isn't a serializable object. Cast to python int

    json_data_to_send = {"prediction": prediction}
    clientsocket.sendall(bytes(json.dumps(json_data_to_send), "UTF-8"))

    # close the client connection
    clientsocket.close()

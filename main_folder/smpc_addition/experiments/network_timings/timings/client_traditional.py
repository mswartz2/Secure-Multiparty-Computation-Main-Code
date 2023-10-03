import socket
import json
import numpy as np
import time
import csv


import sys
import os

sys.path.append(os.getcwd())
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)


def run_trial_centralized(data_point):
    start_time = time.time()
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))
    initial_network_connection_finished = time.time()

    # send data
    json_to_send = {
        "data": data_point,
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))

    server_response = json.loads(clientsocket.recv(1024).decode("UTF-8"))
    client_received_time = time.time()

    clientsocket.close()

    timing_results = server_response

    del timing_results["prediction"]

    timing_results["start_time"] = start_time
    timing_results[
        "initial_network_connection_finished"
    ] = initial_network_connection_finished
    timing_results["client_received_time"] = client_received_time

    return timing_results


# load in dataset
complete_data_set = read_in_pickle_file(
    "main_folder\\smpc_addition\\Data\\CompleteDataSetFeatures.pickle"
)
data_point = complete_data_set.data[0]

timings_to_write_to_file = []

for i in range(100):
    print(f"On trial {i}")
    results = run_trial_centralized(data_point)
    timings_to_write_to_file.append(results)

# print(results)

save_timing_file = "timing_results_traditional.csv"


with open(save_timing_file, "w", newline="") as f:
    title = [x for x in timings_to_write_to_file[0].keys()]
    cw = csv.DictWriter(
        f, title, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    cw.writeheader()
    cw.writerows(timings_to_write_to_file)

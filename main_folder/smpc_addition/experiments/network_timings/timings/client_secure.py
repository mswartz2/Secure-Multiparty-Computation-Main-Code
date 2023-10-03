import socket
import json
import time
import csv
import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)
from main_folder.smpc_addition.network_nodes.ClientSmpcAddition import (
    ClientSmpcAddition,
)


def run_trial_centralized(id, data_point):
    client = ClientSmpcAddition()
    start_time = time.time()
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))
    initial_network_connection_finished = time.time()

    f_shares_server, x_points = client.setup(data_point)
    client_setup_finished_time = time.time()

    # send data
    json_to_send = {
        "x_points": x_points,
        "f_shares_server": f_shares_server,
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))

    results = ""

    while True:
        received_from_server = clientsocket.recv(1024)
        if not received_from_server:
            break
        results += received_from_server.decode("UTF-8")

    json_data_received = json.loads(results)
    client_received_time = time.time()

    clientsocket.close()

    g_shares_client_all_records = json_data_received["g_shares_client_all_records"]
    h_shares_client_all_records = json_data_received["h_shares_client_all_records"]
    s_shares_server_all_records = json_data_received["s_shares_server_all_records"]
    labels = json_data_received["labels"]
    prediction = client.get_prediction(
        g_shares_client_all_records,
        h_shares_client_all_records,
        s_shares_server_all_records,
        labels,
    )
    client_computation_finish_time = time.time()

    timing_results = json_data_received
    del timing_results["g_shares_client_all_records"]
    del timing_results["h_shares_client_all_records"]
    del timing_results["s_shares_server_all_records"]
    del timing_results["labels"]

    timing_results["start_time"] = start_time
    timing_results[
        "initial_network_connection_finished"
    ] = initial_network_connection_finished

    timing_results["client_setup_finished_time"] = client_setup_finished_time
    timing_results["client_received_time"] = client_received_time
    timing_results["client_computation_finish_time"] = client_computation_finish_time

    return timing_results


# load in dataset
complete_data_set = read_in_pickle_file(
    "main_folder\\smpc_addition\\Data\\CompleteDataSetFeatures.pickle"
)
data_point = complete_data_set.data[0]

timings_to_write_to_file = []

for i in range(100):
    print(f"On trial {i}")
    results = run_trial_centralized(i, data_point)
    timings_to_write_to_file.append(results)

# print(results)

save_timing_file = "timing_results_secure.csv"


with open(save_timing_file, "w", newline="") as f:
    title = [x for x in timings_to_write_to_file[0].keys()]
    cw = csv.DictWriter(
        f, title, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    cw.writeheader()
    cw.writerows(timings_to_write_to_file)

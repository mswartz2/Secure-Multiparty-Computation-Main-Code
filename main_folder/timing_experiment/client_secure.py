import socket
import json
import time
import csv
import numpy as np

from PickleFileUtils import read_in_pickle_file
from network_nodes import ClientSecure


def run_trial_centralized(id, data_point):
    client = ClientSecure()
    start_time = time.time()
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))
    client_connection_finished_time = time.time()

    client_setup_start_time = time.time()
    client.setup(data_point)
    client_setup_finished_time = time.time()
    # send data
    json_to_send = {
        "trial_id": id,
        "data": data_point,
        "x_points": client.x_points,
        "f_2_share": client.f_values[1],
        "f_3_share": client.f_values[2],
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))

    results = ""

    while True:
        received_from_server = clientsocket.recv(1024)
        if not received_from_server:
            break
        results += received_from_server.decode("UTF-8")

    results = json.loads(results)

    # results = json.loads(clientsocket.recv(1024).decode("UTF-8"))

    results["client_received_time"] = time.time()

    clientsocket.close()

    client_computation_start_time = time.time()
    g_1_arr = np.array(results["g_1_arr"])
    s_2_arr = np.array(results["s_2_arr"])
    s_3_arr = np.array(results["s_3_arr"])
    labels = np.array(results["labels"])

    prediction = client.get_prediction(g_1_arr, s_2_arr, s_3_arr, labels)

    client_computation_finish_time = time.time()

    results["start_time"] = start_time
    results["client_connection_finished_time"] = client_connection_finished_time
    results["client_setup_start_time"] = client_setup_start_time
    results["client_setup_finished_time"] = client_setup_finished_time
    results["client_computation_start_time"] = client_computation_start_time
    results["client_computation_finish_time"] = client_computation_finish_time
    results["prediction"] = prediction

    return results


# load in dataset
complete_data_set = read_in_pickle_file("CompleteDataSetFeatures.pickle")
data_point = complete_data_set.data[0]

results_to_write_to_file = []

for i in range(1000):
    print(f"On trial {i}")
    results = run_trial_centralized(i, data_point)
    # remove these columns so we can write to a csv easier
    rem_list = [
        "data",
        "x_points",
        "g_1_arr",
        "f_2_share",
        "f_3_share",
        "s_2_arr",
        "s_3_arr",
        "labels",
    ]

    for key in rem_list:
        del results[key]

    results_to_write_to_file.append(results)

# print(results)

save_timing_file = "timing_results_secure.csv"


with open(save_timing_file, "w", newline="") as f:
    # title = "time,SOURCE,PLACE,TEMP,LIGHT,HUMIDITY".split(",") # quick hack
    title = [x for x in results_to_write_to_file[0].keys()]
    cw = csv.DictWriter(
        f, title, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    cw.writeheader()
    cw.writerows(results_to_write_to_file)

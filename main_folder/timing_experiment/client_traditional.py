import socket
import json
import time
import csv

from PickleFileUtils import read_in_pickle_file


def run_trial_centralized(id, data_point):
    start_time = time.time()
    # create a socket object
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = socket.gethostname()
    PORT = 9999

    # connection to hostname on the port.
    clientsocket.connect((HOST, PORT))
    client_connection_finished_time = time.time()
    # send data
    json_to_send = {
        "id": id,
        "data": data_point,
    }
    clientsocket.sendall(bytes(json.dumps(json_to_send), "UTF-8"))

    server_response = json.loads(clientsocket.recv(1024).decode("UTF-8"))

    server_response["client_received"] = time.time()
    server_response["start_time"] = start_time
    server_response["client_connection_finished_time"] = client_connection_finished_time

    clientsocket.close()

    return server_response


# load in dataset
complete_data_set = read_in_pickle_file("CompleteDataSetFeatures.pickle")
data_point = complete_data_set.data[0]

results_to_write_to_file = []

for i in range(1000):
    results = run_trial_centralized(i, data_point)
    # remove the data column so we can write to a csv easier
    del results["data"]
    results_to_write_to_file.append(results)

# print(results)

save_timing_file = "timing_results_traditional.csv"


with open(save_timing_file, "w", newline="") as f:
    # title = "time,SOURCE,PLACE,TEMP,LIGHT,HUMIDITY".split(",") # quick hack
    title = [x for x in results_to_write_to_file[0].keys()]
    cw = csv.DictWriter(
        f, title, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
    )
    cw.writeheader()
    cw.writerows(results_to_write_to_file)

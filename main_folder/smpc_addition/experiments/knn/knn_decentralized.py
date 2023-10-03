from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, accuracy_score
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
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
from main_folder.smpc_addition.network_nodes.ServerSmpcAddition import (
    ServerSmpcAddition,
)


def run_trial(X_train, X_test, y_train, client, server):
    server.set_records_labels(X_train, y_train)
    y_pred = []
    count = 0
    for x in X_test:
        print("Row: ", count)
        count += 1
        f_shares_server, x_points = client.setup(x, rand_range=100000)
        (
            g_shares_client_all_records,
            h_shares_client_all_records,
            s_shares_server_all_records,
            labels,
        ) = server.get_values_for_client(x_points, f_shares_server)
        pred = client.get_prediction(
            g_shares_client_all_records,
            h_shares_client_all_records,
            s_shares_server_all_records,
            labels,
        )
        y_pred.append(pred)
    return y_pred


def get_stats(y_pred, y_test):
    f1_binary = f1_score(y_test, y_pred, average="binary")
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    return f1_binary, accuracy, recall, precision


# testing
def test_and_write_results_to_file(saved_file_path, rand_range=100000):
    write_to_pickle_file([4, 5, 6], saved_file_path)
    num_neighbors = 9
    num_folds = 10

    complete_data_set = read_in_pickle_file(
        "main_folder\\smpc_addition\\Data\\CompleteDataSetFeatures.pickle"
    )
    # get labels
    labels = complete_data_set.labels
    # get data
    data = complete_data_set.data

    X = np.array(data)
    y = np.array(labels)

    stratifiedKFold = StratifiedKFold(n_splits=num_folds, shuffle=True, random_state=86)

    client = ClientSmpcAddition(num_neighbors)
    server = ServerSmpcAddition()

    y_preds = []
    y_tests = []
    count = 1
    for train_index, test_index in stratifiedKFold.split(X, y):
        print("On fold ", count)
        count += 1
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        y_pred = run_trial(X_train, X_test, y_train, client, server)
        y_preds.append(y_pred)
        y_tests.append(y_test)
        print(get_stats(y_pred, y_test))

    y_preds_flattened = [item for sublist in y_preds for item in sublist]
    y_tests_flattened = [item for sublist in y_tests for item in sublist]
    results = {"y_pred": y_preds_flattened, "y_test": y_tests_flattened}

    write_to_pickle_file(results, saved_file_path)


def get_results_from_file(saved_file_path):
    results = read_in_pickle_file(saved_file_path)
    y_pred = results.get("y_pred")
    y_test = results.get("y_test")

    f1_binary, accuracy, precision, recall = get_stats(y_pred, y_test)
    print(f1_binary, accuracy, precision, recall)


save_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\knn\\results\\"

saved_file_path = f"{save_folder}2017_decentralized_preds_withhn.pickle"


test_and_write_results_to_file(saved_file_path)
print("average stats:")
get_results_from_file(saved_file_path)

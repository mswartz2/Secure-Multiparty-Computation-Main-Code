from os import chdir, getcwd
import sys

sys.path.append(getcwd())

from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedKFold
import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)


def get_stats(y_pred, y_test):
    f1_binary = f1_score(y_test, y_pred, average="binary")
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    return f1_binary, accuracy, recall, precision


# testing
def test_and_write_results_to_file(saved_file_path):
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

    y_preds = []
    y_tests = []
    count = 1
    for train_index, test_index in stratifiedKFold.split(X, y):
        print("On fold ", count)
        count += 1
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        knnModel = KNeighborsClassifier(
            n_neighbors=num_neighbors, p=2, weights="uniform", algorithm="auto"
        )
        knnModel.fit(X_train, y_train)
        y_pred = knnModel.predict(X_test)

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

saved_file_path = f"{save_folder}2017_centralized_preds.pickle"


test_and_write_results_to_file(saved_file_path)
print("average stats:")
get_results_from_file(saved_file_path)

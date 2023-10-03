from networkNodes.ClientSmpcAddition import ClientSmpcAddition
from networkNodes.ServerSmpcAddition import ServerSmpcAddition
from math import sqrt
from sklearn.datasets import load_iris
from sklearn.utils import shuffle
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

num_neighbors = 3
client = ClientSmpcAddition(num_neighbors=num_neighbors)
server = ServerSmpcAddition()


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


def run_trial(X_train, X_test, y_train):
    server.set_records_labels(X_train, y_train)
    y_pred = []
    for x in X_test:
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


# get iris dataset
X_class, y_class = load_iris().data, load_iris().target

# we just want binary classification
X_class = X_class[:100]
y_class = y_class[:100]

numFolds = 10
stratifiedKFold = StratifiedKFold(n_splits=numFolds, shuffle=True, random_state=87)

count = 1

X = X_class
y = y_class

y_tests = []
y_preds = []

for train_index, test_index in stratifiedKFold.split(X, y):
    print("On fold: ", count)
    count += 1
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    y_preds.append(run_trial(X_train, X_test, y_train))
    y_tests.append(y_test)

y_preds = np.array(y_preds).flatten()
y_tests = np.array(y_tests).flatten()

print(get_stats(y_preds, y_tests))

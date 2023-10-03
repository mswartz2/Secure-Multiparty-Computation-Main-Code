from sklearn.svm import SVC
from sklearn.metrics import (
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    confusion_matrix,
)
import matplotlib.pyplot as plt

import os
import sys

sys.path.append(os.getcwd())
from main_folder.smpc_addition.PickleFileUtils import (
    read_in_pickle_file,
    write_to_pickle_file,
)


def generate_accuracy_stats(y_pred, y_test, title):
    f1_binary = f1_score(y_test, y_pred, average="binary")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    print(
        f"{title}:\n\tf1: {f1_binary:.4}\n\taccuracy: {accuracy:.4}\n\tprecision: {precision:.4}\n\trecall: {recall:.4}"
    )


def generate_confusion_matrix(y_pred, y_test, save_file_path):
    conf_matrix = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(
                x=j, y=i, s=conf_matrix[i, j], va="center", ha="center", size="xx-large"
            )

    plt.xlabel("Predictions", fontsize=18)
    plt.ylabel("Actuals", fontsize=18)

    plt.savefig(save_file_path + ".png")


def read_in_file(file_name):
    results = read_in_pickle_file(file_name)
    y_pred = results.get("y_pred")
    y_test = results.get("y_test")

    return y_pred, y_test


print("Comparing KNN Results")

save_folder = "c:\\Users\\swart\\Desktop\\secure-mpc-main\\main_folder\\smpc_addition\\experiments\\knn\\results\\"

saved_file_path_centralized = f"{save_folder}2017_centralized_preds.pickle"
saved_file_path_decentralized = f"{save_folder}2017_decentralized_preds_withhn.pickle"

y_pred_centralized, y_test_centralized = read_in_file(saved_file_path_centralized)
y_pred_decentralized, y_test_decentralized = read_in_file(saved_file_path_decentralized)


generate_accuracy_stats(
    y_pred_centralized, y_test_centralized, "Centralized KNN Results"
)
generate_accuracy_stats(
    y_pred_decentralized,
    y_test_decentralized,
    "Decentralized KNN Results - 2 degree, 3 shares",
)


generate_confusion_matrix(
    y_pred_centralized, y_test_centralized, f"{save_folder}cf_centralized"
)

generate_confusion_matrix(
    y_pred_decentralized, y_test_decentralized, f"{save_folder}cf_decentralized"
)

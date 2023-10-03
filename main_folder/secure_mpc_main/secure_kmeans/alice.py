import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
from kmeans import KMeans
import time

style.use('ggplot')

df = pd.read_csv("../data/ipl.csv")

df = df[['one', 'two']]

data = df.values

D = 40
alice_data = data[:D]


def centralized_with_encryption():
    pass
    # encrypt the alice's dataset and send that to the server.
    # bob's node would do the same
    # the server would compute the decrypt the k-means and the centroids(centers) to bob and alice

def centralized_kmeans():
    km = KMeans(k=3)
    print("Alice computing centralized kmeans...")
    km.fit(data)

    colors = 10 * ["r", "g", "c", "b", "k"]

    for centroid in km.centroids:
        plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s=130, marker="x")

    for classification in km.classes:
        color = colors[classification]
        for features in km.classes[classification]:
            plt.scatter(features[0], features[1], color=color, s=30)

    print("Kmeans figure saved in /images/")

    plt.savefig("images/alice-compute-kmeans.png", dpi=150)


def secure_kmeans_computation():
    km = KMeans(k=3, secure=True)
    print("Alice computing kmeans with bob's centroids...")
    km.fit(alice_data)

    colors = 10 * ["r", "g", "c", "b", "k"]

    for centroid in km.centroids:
        plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s=130, marker="x")

    for classification in km.classes:
        color = colors[classification]
        for features in km.classes[classification]:
            plt.scatter(features[0], features[1], color=color, s=30)

    print("Kmeans figure saved in /images/")

    plt.savefig("images/alice-secure-kmeans.png", dpi=150)


def secure_kmeans_for_data_point_classification():
    km = KMeans(k=3, secure=True)
    print("Alice classifying her data points using kmeans with bob's training...")
    colors = 10 * ["r", "g", "c", "b", "k"]

    for point in alice_data:
        classification = km.secure_pred(point)

        color = colors[classification]
        plt.scatter(point[0], point[1], color=color, s=30)

    print("Kmeans figure saved in /images/")
    plt.savefig("images/alice-kmeans-classification.png", dpi=150)


# execution start time
start_time = time.time()

# centralized in to single node
# centralized_kmeans()

# Partial k-means
# secure_kmeans_computation()

# K-means on shares
secure_kmeans_for_data_point_classification()

end_time = time.time()
elapsed = end_time - start_time
print(f"--- {elapsed}s seconds elapsed ---")

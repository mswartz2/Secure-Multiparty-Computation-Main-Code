from network import Server, NetworkShare, node_callback
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd

from kmeans import KMeans

style.use('ggplot')

df = pd.read_csv("../data/ipl.csv")

df = df[['one', 'two']]

data = df.values
km = KMeans(k=3)

D = 40
bob_data = data[D:]

km.fit(bob_data)

colors = 10 * ["r", "g", "c", "b", "k"]

for centroid in km.centroids:
    plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s=130, marker="x")

for classification in km.classes:
    color = colors[classification]
    for features in km.classes[classification]:
        plt.scatter(features[0], features[1], color=color, s=30)

plt.savefig("images/bob-kmeans.png", dpi=150)


host = Server()

node = NetworkShare(name="Bob", node_id=2, k=3)

initial_data = km.centroids
host.receive(node=node, callback=node_callback, initial_data=initial_data)

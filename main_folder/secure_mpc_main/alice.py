from sklearn import datasets
from kmeans import split_data
from network import Client
from node import compute_secure_kmeans

iris = datasets.load_iris()

data, _ = split_data(raw_data=iris.data, split_size="50%")
node = Client(port=9999, name="Alice")

compute_secure_kmeans(data=data, node=node)

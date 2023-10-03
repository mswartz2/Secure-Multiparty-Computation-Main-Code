from network import Server, server_callback, ShamirShare
from sklearn.datasets import load_iris
from kmeans import split_data
from sklearn.utils import shuffle

# get iris dataset
X_class, y_class = load_iris().data, load_iris().target

# we just want binary classification
X_class = X_class[:100]
y_class = y_class[:100]

X_class, y_class = shuffle(X_class, y_class, random_state=20)
X_class_server, y_class_server = X_class[:90], y_class[:90]


centroids = compute_kmeans(data=data, plot=True, plotname="server-kmeans")
print(f"server centroids: {centroids}")

host = Server(port=9999)

node = ShamirShare(name="Server", node_id=2, n=2, k=2)
node.data["global_centroids"] = dict()

host.receive(callback=server_callback, node=node, initial_data=centroids)

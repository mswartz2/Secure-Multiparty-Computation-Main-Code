from network import Server, server_callback, ShamirShare
from sklearn import datasets
from kmeans import compute_kmeans, split_data

iris = datasets.load_iris()

data, _ = split_data(raw_data=iris.data, split_size="50%")

centroids = compute_kmeans(data=data, plot=True, plotname="server-kmeans")
print(f"server centroids: {centroids}")

host = Server(port=9999)

node = ShamirShare(name="Server", node_id=2, n=2, k=2)
node.data['global_centroids'] = dict()

host.receive(callback=server_callback, node=node, initial_data=centroids)

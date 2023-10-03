import numpy as np
from network import NetworkShare, NetworkNode, reconstruct, merge
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')


def euclidean_distance(X, Y):
    dist = 0
    for i in range(len(X)):
        dist += (X[i] - Y[i]) ** 2
    return np.sqrt(dist)


def secure_euclidean_distance(point, index):
    n = 2
    t = 2
    k = 3

    # Alice will use tcp-cient.py (client.py)
    alice = NetworkShare(name="Alice", node_id=1, k=k)
    alice.create_shares(data=point)

    # Bob will use tcp-server.py (server.py)
    bob = NetworkNode(name="Bob", k=3, node_id=2)
    bob.create_shares(index=index)

    # Assisting in secure computation
    server = NetworkNode(name="Server", port=9997, k=3, node_id=3, is_server=True)
    # Server will use tcp-server.py (server.py)
    #
    # alice
    alice_received_from_bob = bob.get_shares_for(node_id=1, share_type="f").get('data')
    alice.merge_shares(shares=alice_received_from_bob, by=merge)

    # bob
    bob_received_from_alice = alice.get_shares_for(node_id=2, share_type="f")
    bob_d = float(bob.merge_shares(node_id=1, shares=bob_received_from_alice, share_type="f").get('data'))
    #
    # # server
    server_received_from_alice = alice.get_shares_for(node_id=3, share_type="f")
    server_d = float(server.merge_with_shares_from(node=bob, shares=server_received_from_alice).get('data'))

    #
    # #
    # # alice reconstruction
    alice_d = alice.get_shares("d")
    d = np.array([alice_d, bob_d, server_d])
    #
    # output
    dist = reconstruct(d)
    return np.sqrt(dist)


class KMeans:
    def __init__(self, k=3, secure=False, epsilon=1e-3, max_iter=500):
        self.k = k  # num  er of clusters
        self.epsilon = epsilon  # tol  rance
        self.classes = {}
        self.max_iter = max_iter  # max  iterations
        self.centroids = {}
        self.secure = secure

    def fit(self, data):
        # initialize centroids
        for i in range(self.k):
            self.centroids[i] = data[i]

        # iterative clustering
        for i in range(self.max_iter):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []
            # find nearest centroid
            for features in data:

                # calculate the distance between data points and a center
                if self.secure is True:
                    distances = [secure_euclidean_distance(features, index) for index in range(self.k)]
                else:
                    distances = [euclidean_distance(features, self.centroids[c]) for c in range(len(self.centroids))]

                # assign each data points to the closest center
                classification = np.argmin(distances)
                self.classes[classification].append(features)

            previous = dict(self.centroids)

            # classify data points into k classes or clusters
            for classification in self.classes:
                self.centroids[classification] = np.average(self.classes[classification], axis=0)

            is_optimal = True

            for centroid in self.centroids:
                original_centroid = previous[centroid]
                current_centroid = self.centroids[centroid]

                if np.sum((current_centroid - original_centroid) / original_centroid * 100.0) > self.epsilon:
                    is_optimal = False

            if is_optimal:
                break

    def pred(self, data):
        # nearest centroid
        distances = [euclidean_distance(data, self.centroids[c]) for c in self.centroids]
        classification = np.argmin(distances)
        return classification

    def pred(self, data, centroids):
        distances = [euclidean_distance(data, centroids[c]) for c in centroids]
        classification = np.argmin(distances)
        return classification

    def secure_pred(self, data):
        # secure nearest centroids
        distances = [secure_euclidean_distance(data, index) for index in range(self.k)]
        classification = np.argmin(distances)
        return classification


colors = 10 * ["r", "g", "c", "b", "k"]


def plot_kmeans(data, centroids, plotname):
    km = KMeans(k=3)
    for centroid in centroids:
        plt.scatter(centroids[centroid][0], centroids[centroid][1], s=130, marker="x")

    for point in data:
        classification = km.pred(data=point, centroids=centroids)

        color = colors[classification]
        plt.scatter(point[0], point[1], color=color, s=30)

    print(f"Kmeans figure saved at /images/{plotname}.png")
    plt.savefig(f"images/{plotname}.png", dpi=150)


def compute_kmeans(data, plot=False, plotname="kmeans"):
    km = KMeans(k=3)
    km.fit(data)

    if plot is True:
        for centroid in km.centroids:
            plt.scatter(km.centroids[centroid][0], km.centroids[centroid][1], s=130, marker="x")

        for classification in km.classes:
            color = colors[classification]
            for features in km.classes[classification]:
                plt.scatter(features[0], features[1], color=color, s=30)

        plt.savefig(f"images/{plotname}.png", dpi=150)

    return km.centroids


def chunks(data, chunk_size):
    '''
    Yield successive chunk size chunks from data"
    '''
    for k in range(0, len(data), chunk_size):
        yield k, data[k:k + chunk_size]


splits = {
    "100%": 1,  # 1 -> 100%, 2 -> 0%
    "50%": 2,  # 1 -> 50%, 2 -> 50%
    "25%": 4  # 1 -> 25%, 2 -> 75%
}


def split_data(raw_data, split_size="50%"):
    '''
    Split data
    '''
    d = splits.get(split_size)
    assert d is not None
    X, Y = np.array([]), np.array([])
    for (k, chunk) in chunks(raw_data, 50):
        data = chunk.copy()
        np.random.shuffle(data)
        size = len(data) // d
        X = np.vstack((X, data[:size])) if len(X) > 0 else data[:size]
        Y = np.vstack((Y, data[size:])) if len(Y) > 0 else data[size:]
    return X, Y

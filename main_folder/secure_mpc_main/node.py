from kmeans import compute_kmeans, plot_kmeans
from network import ShamirShare, merge_sum, interpolate
import json
import numpy as np


def compute_secure_kmeans(data, node):
    centroids = compute_kmeans(data=data)
    print(f"alice centroids: {centroids}")

    shamir = ShamirShare(name=node.name, node_id=1, n=2, k=2)

    global_centroids = dict()

    for (index, centroid) in centroids.items():
        print(f"centroid: {centroid}")
        shamir.create_shares(data=centroid)
        print(f"centroid shares: {shamir.shares}")
        server_shares = shamir.get_shares_for(node_id=2, share_type="f")
        server_shares = server_shares.tolist()
        print(f"shares to send: {server_shares}, len: {len(server_shares)}")

        response = node.send(f"method=send_centroid_shares;shares={json.dumps(server_shares)};index={index};node_id=1")
        print(f"response: {response}")
        response_dict = json.loads(response)
        server_data = response_dict.get("data")
        server_d = json.loads(server_data.get("d"))
        server_g = json.loads(server_data.get("g"))
        shamir.merge_shares(shares=server_g, by=merge_sum)
        node_d = shamir.get_shares("d")
        print(f"alice shares: {shamir.shares}")
        d = np.vstack((node_d, server_d)).T
        global_centroids[index] = 0.5 * interpolate(d)
        response = node.send(f"method=send_centroid_shares_d;d={json.dumps(node_d.tolist())};index={index};node_id=1")
        print(f"response: {response}")
        print(f"d: {d}")

    print(f"global centroids: {global_centroids}")
    plot_kmeans(data=data, centroids=global_centroids, plotname=f"{node.name}-global-kmeans")


    def compute_secure_knn(data, node):
        pass

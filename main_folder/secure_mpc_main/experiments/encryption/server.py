from network import Server, server_callback, NetworkData
from kmeans import compute_kmeans

host = Server()

node = NetworkData(name="Server", compute=compute_kmeans)

host.receive(callback=server_callback, node=node)

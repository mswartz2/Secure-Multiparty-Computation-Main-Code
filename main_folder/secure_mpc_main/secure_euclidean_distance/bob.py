from network import Server, NetworkShare, node_callback

host = Server()

# bob
node = NetworkShare("Bob", node_id=2, k=3)


host.receive(node=node, callback=node_callback)

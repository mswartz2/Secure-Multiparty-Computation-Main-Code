from network import Server, NetworkShare, node_callback

host = Server(port=9997)

# server
node = NetworkShare(name="Server", node_id=3, k=3)

initial_data = []

host.receive(node=node, callback=node_callback, initial_data=initial_data)
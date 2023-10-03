from network import NetworkNode, NetworkShare, merge, reconstruct
import numpy as np

n = 2
t = 2
k = 3

# Alice will use tcp-cient.py (client.py)
alice = NetworkShare("Alice", node_id=1, k=k)
alice.create_shares(data=[4, 2])

# Bob will use tcp-server.py (server.py)
bob = NetworkNode("Bob", k=3, node_id=2)

# Assisting in secure computation
server = NetworkNode("Server", port=9997, k=3, node_id=3, is_server=True)
# Server will use tcp-server.py (server.py)
#
# alice
alice_received_from_bob = bob.get_shares_for(node_id=1, share_type="f").get("data")
print(f"received: {alice_received_from_bob}")
alice.merge_shares(shares=alice_received_from_bob, by=merge)
print(f"alice shares: {alice.shares}")
print(f"alice d: {alice.get_shares('d')}")

# bob
bob_received_from_alice = alice.get_shares_for(node_id=2, share_type="f")
print(f"bob received: {bob_received_from_alice}")
bob_d = int(
    bob.merge_shares(node_id=1, shares=bob_received_from_alice, share_type="f").get(
        "data"
    )
)
print(f"bob d: {bob_d}")
#
# # server
server_received_from_alice = alice.get_shares_for(node_id=3, share_type="f")
server_d = int(
    server.merge_with_shares_from(node=bob, shares=server_received_from_alice).get(
        "data"
    )
)
print(f"server d: {server_d}")

#
# #
# # alice reconstruction
alice_d = alice.get_shares("d")
d = np.array([alice_d, bob_d, server_d])
#
# output
dist = reconstruct(d)
print(f"distance: {np.sqrt(dist)}")

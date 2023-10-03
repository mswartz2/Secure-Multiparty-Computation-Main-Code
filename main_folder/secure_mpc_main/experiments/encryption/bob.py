import pandas as pd
from EncNode import send_encrypted, receive_centroids
from network import Client

df = pd.read_csv("../../data/ipl.csv")

df = df[['one', 'two']]

data = df.values

node = Client(port=9999)

send_encrypted(node=node, raw_data=data, split_size="50%", node_id=2)

receive_centroids(node)


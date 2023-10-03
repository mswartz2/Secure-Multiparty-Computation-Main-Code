from sklearn.datasets import load_iris
from sklearn.utils import shuffle
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd
import numpy as np
from math import sqrt
from network_knn import NetworkNode, NetworkShare, merge, reconstruct


a = [0, 0]

alice = NetworkShare("Alice", node_id=1, k=2)
alice_shares = alice.create_shares(data=a)
print("Alice shares:", alice_shares)

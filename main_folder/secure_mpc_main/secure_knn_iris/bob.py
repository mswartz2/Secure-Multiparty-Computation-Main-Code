from sklearn.datasets import load_iris
from network import Client
from node import compute_secure_knn
from sklearn.utils import shuffle
from node import compute_secure_knn


# get iris dataset
X_class, y_class = load_iris().data, load_iris().target

# we just want binary classification
X_class = X_class[:100]
y_class = y_class[:100]

X_class, y_class = shuffle(X_class, y_class, random_state=20)
X_class_bob, y_class_bob = X_class[95:100], y_class[95:100]

node = Client(port=9999, name="Bob")

compute_secure_knn(X_class=X_class_bob, node=node)

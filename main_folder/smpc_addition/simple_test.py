from network_nodes.ClientSmpcAddition import ClientSmpcAddition
from network_nodes.ServerSmpcAddition import ServerSmpcAddition
from math import sqrt

client = ClientSmpcAddition(num_neighbors=3)
server = ServerSmpcAddition()


def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)):
        distance += (row1[i] - row2[i]) ** 2
    return sqrt(distance)


test_point = [1, 2, 3, 4, 5]

server_points = [
    [6, 7, 8, 9, 10],
    [2, 3, 7, 5, 4],
    [38, 349, 2348, 342, 0],
    [3, 7, 2, 5, 1],
    [123, 123, 123, 151, 224],
]

# test_point = [0, 5]
# server_points = [[3, 9], [4, 3], [82, 34]]

server_labels = [0, 0, 1, 0, 1]

server.set_records_labels(server_points, server_labels)
f_shares_server, x_points = client.setup(test_point, rand_range=10000)

(
    g_shares_client_all_records,
    h_shares_client_all_records,
    s_shares_server_all_records,
    labels,
) = server.get_values_for_client(x_points, f_shares_server)


for row in server_points:
    print("Traditional Distance: ", euclidean_distance(test_point, row))


client._distance_computation(
    g_shares_client_all_records,
    h_shares_client_all_records,
    s_shares_server_all_records,
)
print("Secure distances: ", client.distances)

print(
    "Prediction: ",
    client.get_prediction(
        g_shares_client_all_records,
        h_shares_client_all_records,
        s_shares_server_all_records,
        labels,
    ),
)

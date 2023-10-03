from basic_networking.server_centralized import ServerCentralized

# from server_centralized import ServerCentralized


class ClientCentralized:
    def __init__(self):
        pass

    def predict_classification(
        self,
        test_row,
        serverNode: ServerCentralized,
    ):
        prediction = serverNode.test_point(test_row)
        return prediction

from sklearn.neighbors import KNeighborsClassifier


class ServerTraditional:
    def __init__(self) -> None:
        super().__init__()
        self.X_train = []
        self.y_train = []
        self.num_neighbors = 9
        self.model = None

    def set_up_model(self, X_train, y_train, num_neighbors):
        self.X_train = X_train
        self.y_train = y_train
        self.num_neighbors = num_neighbors
        self._train_model_knn()

    def _train_model_knn(self):
        self.model = KNeighborsClassifier(
            n_neighbors=self.num_neighbors, p=2, weights="uniform", algorithm="auto"
        )
        self.model.fit(self.X_train, self.y_train)

    def test_point(self, test_row):
        prediction = self.model.predict([test_row])
        return prediction[0]

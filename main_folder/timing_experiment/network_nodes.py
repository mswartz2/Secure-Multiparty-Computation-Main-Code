from sklearn.neighbors import KNeighborsClassifier
import random
from scipy.interpolate import lagrange
import numpy as np


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

class RandPoly:
    """
    Random and zero free coefficient polynomial
    """

    def __init__(self, n, name='', R = None, fzc=False, p = 1337):
        self.name = name
        self.n = n
        self.p = p
        self.fzc = fzc # free zero coefficient
        if R:
            self.R = R
            # assert(len(R) == n)
        else: 
            self.R = [0] * (n+1) 
            for t in range(self.n+1):
                if t == 0 and fzc is True:
                    self.R[t] = (t, 0)
                else:
                    r = random.randint(1,self.p)
                    self.R[t] = (t, r)

    def poly(self, x):
        s = 0
        for (n, r) in self.R:
            s += r * x ** n
        return s

    
    def poly_str(self):
        """
        outputs the underlying polynomial
        """
        s = ""
        first_zero = self.R[0][1] == 0
        if first_zero:
            for (i, r) in self.R:
                if i == 0:
                    continue
                elif i == 1:
                    s +=  f"{r}x" 
                else:
                    s += f"+{r}x^{i}"
        else:
            for (i, r) in self.R:
                if i == 0:
                    s += f"{r}"
                elif i == 1:
                    s +=  f"+{r}x" 
                else:
                    s += f"+{r}x^{i}"
        if self.name:
            return f"{self.name}(x)={s}"
        else:
            return s

    def __str__(self):
        return self.poly_str()

    def __repr__(self):
        return self.poly_str()

    def __add__(self, other):
        n = min(len(self.R), len(other.R))
        m = max(len(self.R), len(other.R))
        R = [0] * m
        for i in range(m):
            if i < n:
                R[i] = (i, self.R[i][1] + other.R[i][1])
            elif i < len(self.R):
                R[i]= (i, self.R[i][1])
            elif i < other.R:
                 R[i][1] = (i, other.R[i][1])
        
        return RandPoly(n=self.n, R=R)

class SmpcNode:
    def __init__(self) -> None:
        pass

    def generate_functions(self, features_arr):
        all_functions = []
        for feature in range(len(features_arr)):
            func = RandPoly(
                name=f"f{feature}",
                n=1,
                R=[
                    (i, x)
                    for i, x in enumerate(
                        list([features_arr[feature], random.randint(2, 250)])
                    )
                ],
            ).poly
            all_functions.append(func)
        return all_functions

    def generate_shares_for_x_value(self, func_array, x):
        shares = []
        for func in func_array:
            shares.append(func(x))
        return shares

    def _get_feature_distances(self, arr1, arr2):
        distances = []
        for feature_a, feature_b in zip(arr1, arr2):
            dist = (feature_a - feature_b) ** 2
            distances.append(dist)
        return distances
        

    def _sum_distances(self, arr):
        return sum(arr)

    def _reconstruct(self, shares, xvals):
        x = xvals
        y = shares
        f = lagrange(x, y)
        return f(0)

    def calc_s_n_arr(self, g_n_arr, f_n):
        distances_arr = []
        s_1_arr = []
        for g_n in g_n_arr:
            distances_arr.append(self._get_feature_distances(g_n, f_n))

        for distances_1 in distances_arr:
            s_1 = self._sum_distances(distances_1)
            s_1_arr.append(s_1)

        return s_1_arr

class ClientSecure(SmpcNode):
    def __init__(self) -> None:
        super().__init__()
        self.data_point = None
        self.three_random_points = []
        self.rand_seed = 72
        self.rand_range = 100000 # max x for lagrange
        self.num_neighbors = 9
        self.f_values = []
        self.x_points = []
        self.s_1_arr = []
        self.s_2_arr = []
        self.s_3_arr = []
        self.label_arr = []
        
    def setup(self, data_point):
        self.data_point = data_point
        polynomials = self.generate_functions(self.data_point)
        # pick 3 random points
        id_1, id_2, id_3 = random.Random(self.rand_seed).sample(range(1, self.rand_range), 3)

        f_1 = self.generate_shares_for_x_value(polynomials, id_1)
        f_2 = self.generate_shares_for_x_value(polynomials, id_2)
        f_3 = self.generate_shares_for_x_value(polynomials, id_3)

        self.f_values = [f_1, f_2, f_3]
        self.x_points = [id_1, id_2, id_3]

    def get_prediction(self, g_1_arr, s_2_arr, s_3_arr, label_arr):
        self.s_1_arr = self.calc_s_n_arr(g_1_arr, self.f_values[0])
        self.s_2_arr = s_2_arr
        self.s_3_arr = s_3_arr
        self.label_arr = label_arr

        neighbors = self._get_neighbors()

        output_values = [row[-1] for row in neighbors]
        prediction = max(set(output_values), key=output_values.count)
        
        return prediction

    def _get_distances_and_labels(self):
        # calculate s_0_arr
        distance_labels_arr = []
        for s_1, s_2, s_3, label in zip(self.s_1_arr, self.s_2_arr, self.s_3_arr, self.label_arr):
            s_0 = self._reconstruct([s_1, s_2, s_3], self.x_points)
            try:
                distance = abs(np.sqrt(s_0))
            except:
                distance = 0

            distance_labels_arr.append((distance, label))

        return distance_labels_arr

    def _get_neighbors(self):
        distances = self._get_distances_and_labels()
        distances.sort(key=lambda tup: tup[0])
        neighbors = list()
        for i in range(self.num_neighbors):
            neighbors.append([distances[i][0], distances[i][1]])
        return neighbors



class ServerSecure(SmpcNode):
    def __init__(self) -> None:
        super().__init__()
        self.features = []
        self.labels = []

    def set_features_labels(self, features, labels):
        self.features = features
        self.labels = labels

    def _generate_functions_for_all_data(self):
        functions_arr = []
        for i in range(len(self.features)):
            functions_arr.append(self.generate_functions(self.features[i]))
        return functions_arr

    def _generate_shares_for_all_data(self, polynomials_arr, x_vals):
        g_1_arr = []
        g_2_arr = []
        g_3_arr = []
        for i in range(len(self.features)):
            g_1_arr.append(
                self.generate_shares_for_x_value(polynomials_arr[i], x_vals[0])
            )
            g_2_arr.append(
                self.generate_shares_for_x_value(polynomials_arr[i], x_vals[1])
            )
            g_3_arr.append(
                self.generate_shares_for_x_value(polynomials_arr[i], x_vals[2])
            )
        return g_1_arr, g_2_arr, g_3_arr

    def get_gn_sn_for_client(self, x_points, f_2_share, f_3_share):
        """Receives the x-values and share for 2 of the x-values
        Returns:
        - array of g(id_1) for all points the server has
        - array of s(id_2) for all points the server has
        - array of s(id_3) for all points the server has
        - array of labels"""


        # generate polynomials for all features for each data point
        polynomials_arr = self._generate_functions_for_all_data()

        # calculate g(n) functions for all data points
        # use x_points as the n values
        g_1_arr, g_2_arr, g_3_arr = self._generate_shares_for_all_data(
            polynomials_arr, x_points
        )

        # calculate s_2_arr and s_3_arr
        s_2_arr = self.calc_s_n_arr(g_2_arr, f_2_share)
        s_3_arr = self.calc_s_n_arr(g_3_arr, f_3_share)

        return g_1_arr, s_2_arr, s_3_arr, self.labels

    
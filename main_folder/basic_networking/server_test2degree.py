from basic_networking.smpc_node_test2degree import SmpcNode


class Server(SmpcNode):
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

    def get_gn_sn_for_client(self, id_1, id_2, id_3, f_2_share, f_3_share):
        """Receives the x value and share for 2 x-values
        Returns:
        - array of g(id_1) for all points the server has
        - array of s(id_2) for all points the server has
        - array of s(id_3) for all points the server has
        - array of labels"""

        # generate polynomials for all features for each data point
        polynomials_arr = self._generate_functions_for_all_data()

        # calculate g(n) functions for all data points
        # use id_1, id_2, and id_3 as the n values
        g_1_arr, g_2_arr, g_3_arr = self._generate_shares_for_all_data(
            polynomials_arr, [id_1, id_2, id_3]
        )

        # calculate s_2_arr and s_3_arr
        s_2_arr = self.calc_s_n_arr(g_2_arr, f_2_share)
        s_3_arr = self.calc_s_n_arr(g_3_arr, f_3_share)

        return g_1_arr, s_2_arr, s_3_arr, self.labels

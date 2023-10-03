from main_folder.smpc_addition.network_nodes.SmpcAdditionNode import SmpcAdditionNode

class ClientSmpcAddition(SmpcAdditionNode):
    def __init__(self, num_neighbors=9) -> None:
        super().__init__()
        self.record = None
        self.rand_seed = 87
        self.rand_range = 0 # max x for lagrange
        self.num_neighbors = num_neighbors

        self.x_points = []
        self.f_shares_client = []
        self.distances = []
        self.label_arr = []

    def setup(self, record, num_shares = 3, rand_range = 100000):
        '''Retruns f_shares_server, x_points'''
        self.record = record
        self.rand_range = rand_range

        f = self.generate_functions(self.record)

        self.x_points = self.get_random_points(num_shares, self.rand_seed, self.rand_range)
        f_shares = self.generate_shares(f, self.x_points)

        self.f_shares_client = [[x[0] for x in f_shares]]
        f_shares_server = [x[1:] for x in f_shares]
    
        return f_shares_server, self.x_points

    def _distance_computation(self,g_shares_client_all_records,h_shares_client_all_records,s_shares_server_all_records):
        '''Returns distances to all points'''
        distances = []
        for record in range(len(g_shares_client_all_records)):
            # print(f'On record {record} of {len(g_shares_client_all_records)}')
            g_shares_client = g_shares_client_all_records[record]
            h_shares_client = h_shares_client_all_records[record]
            s_shares_server = s_shares_server_all_records[record]
            
            s_shares_client = self.calc_share_sums_one_record(
                self.f_shares_client, g_shares_client, h_shares_client
            )

            lagrange_set_one_record = self.get_set_of_lagrange_values_one_record(s_shares_client, s_shares_server)
            distance = self.distance_to_one_point(lagrange_set_one_record, self.x_points)
            distances.append(distance)
        self.distances = distances
    
    def _get_neighbors(self, labels):
        distances_with_labels = [(self.distances[i], labels[i]) for i in range(len(labels))]
        distances_with_labels.sort(key=lambda tup: tup[0])
        neighbors = list()
        for i in range(self.num_neighbors):
            neighbors.append([distances_with_labels[i][0], distances_with_labels[i][1]])
        return neighbors
    
    def get_prediction(self, g_shares_client_all_records,h_shares_client_all_records,s_shares_server_all_records, labels):
        '''Returns predicted classification'''
        self.labels = labels

        self._distance_computation(g_shares_client_all_records, h_shares_client_all_records, s_shares_server_all_records)
        neighbors = self._get_neighbors(labels)

        output_values = [row[-1] for row in neighbors]
        prediction = max(set(output_values), key=output_values.count)
        
        return prediction
        
from main_folder.smpc_addition.network_nodes.SmpcAdditionNode import SmpcAdditionNode


class ServerSmpcAddition(SmpcAdditionNode):
    def __init__(self) -> None:
        super().__init__()
        self.records = []
        self.labels = []
        self.g_shares_all_recs = []
        self.h_shares_all_recs = []

    def set_records_labels(self, records, labels):
        self.records = records
        self.labels = labels

    def _generate_functions_and_shares_for_all_records(self, x_points):
        g_shares_all_recs = []
        h_shares_all_recs = []
        for record in self.records:
            # make all features negative to do subtraction
            record = [x * -1 for x in record]
            g = self.generate_functions(record)
            # h(n) will have all features = 0 for all records
            h = self.generate_functions([0 for x in record])

            g_shares = self.generate_shares(g, x_points)
            h_shares = self.generate_shares(h, x_points)

            g_shares_all_recs.append(g_shares)
            h_shares_all_recs.append(h_shares)

        self.g_shares_all_recs = g_shares_all_recs
        self.h_shares_all_recs = h_shares_all_recs

    def get_values_for_client(self, x_points, f_shares_server):
        """Returns:
        g_shares_client_all_records,
        h_shares_client_all_records,
        s_shares_server_all_records,
        labels"""
        self._generate_functions_and_shares_for_all_records(x_points)

        g_shares_client_all_records = []
        h_shares_client_all_records = []
        s_shares_server_all_records = []

        for record in range(len(self.g_shares_all_recs)):
            g_shares_client = [[x[0] for x in self.g_shares_all_recs[record]]]
            g_shares_server = [x[1:] for x in self.g_shares_all_recs[record]]

            h_shares_client = [[x[0] for x in self.h_shares_all_recs[record]]]
            h_shares_server = [x[1:] for x in self.h_shares_all_recs[record]]

            s_shares_server = self.calc_share_sums_one_record(
                f_shares_server, g_shares_server, h_shares_server
            )

            g_shares_client_all_records.append(g_shares_client)
            h_shares_client_all_records.append(h_shares_client)
            s_shares_server_all_records.append(s_shares_server)

        return (
            g_shares_client_all_records,
            h_shares_client_all_records,
            s_shares_server_all_records,
            self.labels,
        )

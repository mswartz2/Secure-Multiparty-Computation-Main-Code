import random
from math import sqrt
from scipy.interpolate import lagrange

from main_folder.smpc_addition.network_nodes.RandPoly import RandPoly

class SmpcAdditionNode:
    def __init__(self) -> None:
        pass

    def generate_functions(self, record):
        all_functions = []
        for feature in record:
            func = RandPoly(
                n=2,
                R=[
                    (i, x)
                    for i, x in enumerate(
                        list(
                            [
                                feature,
                                random.randint(2, 250),
                                random.randint(2, 250),
                            ]
                        )
                    )
                ],
            ).poly
            all_functions.append(func)
        return all_functions

    def generate_shares(self, func_array, x_points):
        shares = []
        for f in func_array:
            x_point_shares = []
            for x in x_points:
                x_point_shares.append(f(x))
            shares.append(x_point_shares)
        return shares
    
    def get_random_points(self, num_points, rand_seed, max_x):
        points = random.Random(rand_seed).sample(range(1, max_x), num_points)
        return points

    def calc_share_sums_one_record(self, f_shares, g_shares, h_shares):
        s_x_points = []
        for x_point in range(len(f_shares)):
            s_x = []
            for i, j, k in zip(f_shares[x_point], g_shares[x_point], h_shares[x_point]):
                sum = i+j+k
                s_x.append(sum)
            s_x_points.append(s_x)
        return s_x_points
    
    def get_set_of_lagrange_values_one_record(self, s_shares_client, s_shares_server):
        lagrange_set_one_record = []
        for feature in range(len(s_shares_client[0])):
            s_x_feature = [s_shares_client[0][feature]]
            for i in range(len(s_shares_server[0])):
                s_x_feature.append(s_shares_server[feature][i])
            lagrange_set_one_record.append(s_x_feature)
        return lagrange_set_one_record
    
    def reconstruct(self, shares, x_points):
        f = lagrange(x_points, shares)
        return f
    
    def distance_to_one_point(self, lagrange_set_one_record, x_points):
        # client interpolation
        s_n_functions = [self.reconstruct(shares, x_points) for shares in lagrange_set_one_record]
        all_s0_vals = [f(0) for f in s_n_functions]

        # calc distance
        distance = 0
        for i in all_s0_vals:
            distance += i**2
        distance = sqrt(distance) 

        return distance
    
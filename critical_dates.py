import pandas as pd

__author__ = 'slei'


class HeuristicTSP:
    """ Finds the shortest path using a heuristic method """

    def __init__(self, df_cities):
        self.df = df_cities
        self.distance = dict([((t.origin, t.destination), t.distance) for t in self.df.itertuples()])
        self.cities = list(set(self.df['destination']))

        self.tour_lst = []
        self.tour_leg_distances_lst = []
        self.total_distance_lst = []

        self.soln_df = None
        self.shortest_tour = None
        self.shortest_tour_leg_distances = None
        self.shortest_distance = None

    def generate_soln_df(self):
        soln_dict = {'tour_lst': self.tour_lst, 'tour_leg_distances_lst': self.tour_leg_distances_lst,
                     'total_distance_lst': self.total_distance_lst}
        self.soln_df = pd.DataFrame(soln_dict)
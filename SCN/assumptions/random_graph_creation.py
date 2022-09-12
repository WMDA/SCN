# SCN imports
import SCN.graphs.permutations as perms
from SCN.graphs.graph_utlis import save_pickle

# Base python imports
import multiprocessing


class Random_Graph_Creator:

    '''
    Class to permuate random graphs for network assumptions.

    Parameters
    ----------
    perms: int of number of permutations
    *data: thresholded graphs 

    Usage
    -----
    from SCN.assumptions.random_graph_creation import Random_Graph_Creator

    graph = Random_Graph_Creator(1000)
    graph.data(group_one_graph_threshold, group_two_graph_threshold, group_three_graph_threshold)
    graph.permutations()

    '''

    def __init__(self, perms: int) -> None:
        
        self.perms = perms

    def data(self, *data) -> None:

        self.data = dict(zip([f'group_{key}'for key in range(len(data))], [group for group in data]))
        self.groups = len(self.data.keys())

    def muti_processing_permutations(self, key):
        
        print(f'\nCreating Random graph for {key}\n')
        graph_threshold = self.data[key]
        perms.random_graph_permutations(graph_threshold, self.perms, key)

    def permutations(self):

        with multiprocessing.Pool(self.groups) as func:
            func.map(self.muti_processing_permutations, self.data.keys())

        
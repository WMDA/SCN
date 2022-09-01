# SCN imports
import SCN.graphs.permutations as perms

# Base python imports
import multiprocessing


class Random_Graph_Creator:

    def __init__(self, perms: int, name:str='graph') -> None:
        
        self.perms = perms
        self.name = name

    def data(self, *data) -> None:
        '''
        Method to read in data

        Parameters
        ----------
        *data: thresholded graphs 
        '''

        self.data = dict(zip([f'group_{key}'for key in range(len(data))], [group for group in data]))
        self.groups = len(self.data.keys())

    def muti_processing_permutations(self, key):
        
        print(f'\nCreating Random graph for {key}\n')
        graph_threshold = self.data[key]
        perms.random_graph_permutations(graph_threshold, self.perms, key)
    
    def permutations(self):

        with multiprocessing.Pool(self.groups) as func:
            func.map(self.muti_processing_permutations, self.data.keys())
        
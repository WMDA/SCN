# SCN imports
import SCN.graphs.graphs as graphs
from SCN.graphs.graph_utlis import save_pickle

# Base python imports
import multiprocessing


def list_of_measures() -> list:
    '''
    Function to get list of graph measures

    Parameters
    ----------
    None

    Returns
    -------
    list: list of graph theory measures
    '''
    return ['average_clustering', 'average_shortest_path_length', 'assortativity', 'modularity', 'efficiency', 'small_world']


class Create_thresholded_graphs:

    '''
    Class to threshold graphs for each group at a set range. Then calculates global measures

    Usage
    -----
    graphs = Create_thresholded_graphs(range(4,100), group_0_dataframe, group_2_dataframe, group_1_dataframe)
    graphs.create()
    measures = graphs.global_measures()
    '''

    def __init__(self, thresholds: int, *data) -> None:

        self.data_dic = self.data_dictionary(*data)
        self.thresholds = thresholds
        self.results = self.results_dictionary_creation(*data)
        self.names = graphs.load_names()
        self.centroids = graphs.load_centroids()

    def data_dictionary(self, *data) -> dict:
        return dict(zip([f'group_{key}'for key in range(len(data))], [group for group in data]))

    def results_dictionary_creation(self, *data) -> dict:
        return dict(zip([f'group_{key}'for key in range(len(data))], [list() for group in data]))

    def thresholding_graphs(self, key) -> None:
        print(f'Creating graphs in the threshold range {self.thresholds} for {key}')

        for threshold in self.thresholds:
            data = self.data_dic[key]
            graph = graphs.create_graphs(
                data, self.names, self.centroids, threshold)
            graph['graph_threshold'].__name__ = f'{key}_graph_threshold_value_{threshold}'
            self.results[f'{key}'].append(graph['graph_threshold'])

    def create(self) -> None:
        for key in self.data_dic.keys():
            self.thresholding_graphs(key)

    def global_measures(self) -> dict:

        print('Calculating global measures for each thresholded graph')
        global_measures_dict = {}
        for keys, values in self.results.items():
            for graph_object in values:
                global_measures = graph_object.calculate_global_measures()
                global_measures_dict[f'{graph_object.__name__}'] = global_measures

        return global_measures_dict


class Test_statstic:
    def __init__(self, global_measures: dict) -> None:
        self.global_measures = global_measures
        self.measures = list_of_measures()

    def create_group_dictionary(self) -> dict:

        import re
        cleaned_keys = [re.sub(r'_graph_threshold_value_.*', '', key) for key in list(self.global_measures.keys())]
        groups = list(set(cleaned_keys))
        return dict(zip(groups, [list() for group in groups]))
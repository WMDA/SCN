# SCN imports
import SCN.graphs.graphs as graphs
from SCN.graphs.graph_utlis import save_pickle

# Base python imports
import multiprocessing


def list_of_measures() -> list:
    '''
    Function to get list of graph measures
    TODO add small_world to functionality

    Parameters
    ----------
    None

    Returns
    -------
    list: list of graph theory measures
    '''
    return ['average_clustering', 'average_shortest_path_length', 'assortativity', 'modularity', 'efficiency']


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

    '''
    Class to caluculate test statistics between each group.

    Usage
    -----
    stats = Test_statstic(global_measures_dictionary)
    test_stats = stats.test_statistic(range(4,100))

    '''

    def __init__(self, global_measures: dict) -> None:
        self.global_measures = global_measures
        self.measures = list_of_measures()

    def create_group_dictionary(self) -> dict:

        import re
        cleaned_keys = [re.sub(r'_graph_threshold_value_.*', '', key) for key in list(self.global_measures.keys())]
        groups = list(set(cleaned_keys))
        
        test_stat_list = []
        for outergroup in groups:
            for innergroup in groups[::-1]:
                if outergroup != innergroup:
                    check_not_in_list = f'{outergroup}/{innergroup}'
                    if '_'.join(check_not_in_list.split('/')[::-1]) not in test_stat_list:
                         test_stat_list.append(f'{outergroup}_{innergroup}') 
        

        return dict(zip([group for group in test_stat_list], [dict() for group in test_stat_list]))

    def test_statistic(self, threshold_values: int) -> dict:
        
        '''
        Calculates test statistics
        '''
        test_statistics = self.create_group_dictionary()
        
        for threshold in threshold_values:
            for measure in self.measures:
                for key in test_statistics:
                    split = key.split('_')
                    groups = [split[0] + '_' + split[1], split[2] + '_' + split[3]]
                    test_stat = self.global_measures[f'{groups[0]}_graph_threshold_value_{threshold}'][measure] - self.global_measures[f'{groups[1]}_graph_threshold_value_{threshold}'][measure]
                    inner_key = f'{measure}_at_threshold_value_{threshold}'
                    test_statistics[key][inner_key] = test_stat
        
        test_statistics_dictionary = self.summary_stat(test_statistics) 
        
        return test_statistics_dictionary

    def summary_stat(self, test_statistics_dictionary) -> dict:
        
        '''
        Creates a list of all values for a measure
        '''

        for group_key in test_statistics_dictionary.keys():
            for measure in self.measures:
                measure_summary = [test_statistics_dictionary[group_key][key] for key in test_statistics_dictionary[group_key] if measure in key]
                test_statistics_dictionary[group_key][measure] = measure_summary
        print(test_statistics_dictionary)
        return test_statistics_dictionary
        
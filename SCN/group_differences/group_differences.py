# SCN imports
import SCN.graphs.graphs as graphs
from SCN.graphs.graph_utlis import save_pickle, list_of_measures

# Base python imports
import numpy as np
import re


class Create_thresholded_graphs:

    '''
    Class to threshold graphs for each group at a set range. Then calculates global measures.

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
        print(
            f'Creating graphs in the threshold range {self.thresholds} for {key}')

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
    Class to calculate test statistics between each group.

    Usage
    -----
    stats = Test_statstic(global_measures_dictionary)
    test_stats = stats.test_statistic(range(4,100))

    '''

    def __init__(self, global_measures: dict) -> None:
        self.global_measures = global_measures
        self.measures = list_of_measures()

    def create_group_dictionary(self) -> dict:

        cleaned_keys = [re.sub(r'_graph_threshold_value_.*', '', key)
                        for key in list(self.global_measures.keys())]
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
                    groups = [split[0] + '_' + split[1],
                              split[2] + '_' + split[3]]
                    test_stat = self.global_measures[f'{groups[0]}_graph_threshold_value_{threshold}'][measure] - \
                        self.global_measures[f'{groups[1]}_graph_threshold_value_{threshold}'][measure]
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
                measure_summary = [test_statistics_dictionary[group_key][key]
                                   for key in test_statistics_dictionary[group_key] if measure in key]
                test_statistics_dictionary[group_key][measure] = measure_summary
        return test_statistics_dictionary


def find_max_null_stat(threshold_value: list, null_distribution: dict, group_key: str, measure_key: str, list_number: int) -> dict:
    '''
    Function to loop through each element in a list for each thresold value.

    Parameters
    ----------
    null_distribution:dict dictionary of null_distribution
    group_key:str dictionary key for group 
    measure_key:str dictionary key for the graph theory measure.
    list_number:int list index of permutation

    Returns
    -------
    max_null_statistic: int max null statistic for that permutation.

    '''

    values = []
    for threshold in threshold_value:
        values.append(
            null_distribution[group_key][f'thresholded_value_{threshold}'][measure_key][list_number])

    max_null_statistic = max(values, key=abs)

    max_null_dict = {
        'summarised_values': values,
        'max_null': max_null_statistic
    }

    return max_null_dict


def maximum_null_stat(null_distribution: dict, threshold_range: int, permutation_range: int) -> dict:
    '''
    Function to get the maximum null statistic across each permutation across all thresholds.

    Parameters
    ---------
    null_distribution: dict of the null distribution
    threshold_range: int range of values the graph was thresholded at.
    permutation_range: int the number of permutations (must be a range)

    Returns
    -------
    null_stat_summarized: dict of maximum null stats
    '''

    null_stat_summarized = dict(zip([group for group in null_distribution.keys()], [
                                dict() for group in null_distribution.keys()]))
    measures = list_of_measures()

    for group_key in null_stat_summarized.keys():
        for measure in measures:
            null_stat_summarized[group_key][measure] = []

    for group_key in null_stat_summarized.keys():
        for perm in permutation_range:
            for measure in measures:
                max_null_statistic = find_max_null_stat(
                    threshold_range, null_distribution, group_key, measure, perm)
                null_stat_summarized[group_key][measure].append(
                    max_null_statistic['max_null'])

    return null_stat_summarized

def critical_value(null_stat_summarized: dict) -> dict:
    '''
    Function to return the critical value for each measure.

    Parameters
    ----------
    null_stat_summarized: dict of summarized null statistics.

    Returns
    -------
    crit_val: dict of critical values for each measure
    '''

    crit_val = dict(zip([group for group in null_stat_summarized.keys()], [
                    dict() for group in null_stat_summarized.keys()]))
    measures = list_of_measures()

    for group_key in null_stat_summarized.keys():
        for measure in measures:
            if max(null_stat_summarized[group_key][measure]) > 0:
                if min(null_stat_summarized[group_key][measure]) < 0:
                    crit_val[group_key][measure] = np.abs(np.quantile(
                        null_stat_summarized[group_key][measure], 0.975))

                if min(null_stat_summarized[group_key][measure]) > 0:
                    crit_val[group_key][measure] = np.quantile(
                        null_stat_summarized[group_key][measure], 0.95)

            if max(null_stat_summarized[group_key][measure]) <= 0:
                crit_val[group_key][measure] = np.quantile(
                    null_stat_summarized[group_key][measure], 0.05)

    return crit_val


def identify_clusters(test_statistics: dict, crit_val: dict, null_stat_summarized: dict) -> dict:
    
    '''
    Function to find if test statistic is greater than critical value.

    Parameters
    ----------
    test_statistics: dict of test_statistic values 
    crit_val: dict of critical values for each measure
    null_stat_summarized: dict of the maximum null stat

    Returns
    -------
    clusters: dict of values greater than critical value, the crticial value and the null distirbution
    '''
    
    clusters = {}

    for group_key in test_statistics.keys():
        for key, val in test_statistics[group_key].items():
            new_key = re.sub(r'_at_threshold_value_.*', '', key)
            critical_value = crit_val[group_key][new_key]
            significance = False
           
            if type(val) != list:
                if critical_value > 0 and val > 0:
                    if val > critical_value:
                        significance = True

                if critical_value < 0 and val < 0:
                    if val < critical_value:
                        significance = True

                else:
                    if np.abs(val) > np.abs(critical_value):
                        significance = True

                if significance == True:
                    clusters[f'{group_key}_{key}'] = {
                        'value': test_statistics[group_key][key],
                        'critical_value': critical_value,
                        'null': null_stat_summarized[group_key][new_key]

                    }
    return clusters

def auc(test_statistics: dict, crit_val: dict, threshold_value: int) -> dict:
    
    '''
    Function to return area under the curve for test statistics

    Parameters
    ----------
    test_statistics: dict of test_statistic values.
    crit_val: dict of critical values for each measure.
    threshold_value: int a range of threshold values graphs were set to.
    
    Returns
    -------
    auc: dict of auc values.
    
    '''

    auc = dict(zip([group for group in test_statistics.keys()], [
                    dict() for group in test_statistics.keys()]))
    
    
    for group_key in auc.keys():
        for measure in list_of_measures():
            
            if all(val >0 for val in test_statistics[group_key][measure]) == False and all(val <0 for val in test_statistics[group_key][measure]) == False:
                test_statistic_list = np.abs(test_statistics[group_key][measure])
                critical = np.abs(crit_val[group_key][measure])
    
            else:
                test_statistic_list = test_statistics[group_key][measure] 
                critical = crit_val[group_key][measure]
                
            threshold_values_linspace = np.linspace(start=min(threshold_value), stop=max(threshold_value), num=500)
            observation_interploated = np.interp(threshold_values_linspace, threshold_value, test_statistic_list)
            observation_interploated -= critical
    
            if  all(val >0 for val in test_statistics[group_key][measure]) == True:
                observation_interploated[observation_interploated<0] = 0
            else:
                observation_interploated[observation_interploated>0] = 0
                
            obs_AUC = np.trapz(threshold_values_linspace, observation_interploated) 
            auc[group_key][measure] = obs_AUC

    return auc

def summarize_null_distribution(null_distribution: dict, threshold_value: int, permuatation_range: int) -> dict:

    '''
    Function to sort null distribution into list for use in the null auc function

    Parameters
    ----------
    null_distribution: dict of the null_distribution values.
    threshold_value: int a range of threshold values graphs were set to.
    permuatation_range: int the range os permuations used.

    Returns
    -------
    summarized_permutations: dict of list of values.

    '''

    summarized_permutations = dict(zip([group for group in null_distribution.keys()], [
                    dict() for group in null_distribution.keys()]))
    
    for group_key in summarized_permutations.keys():
        for measure in list_of_measures():
            summarized_permutations[group_key][measure] = []
    
    for group_key in summarized_permutations.keys():
        for perm in permuatation_range:
            for measure in list_of_measures():
                max_null_statistic_values = find_max_null_stat(threshold_value, null_distribution, group_key, measure, perm )
                summarized_permutations[group_key][measure].append(max_null_statistic_values['summarised_values'])

    return summarized_permutations
    
def null_auc(null_distribution: dict, threshold_value: int, permuatation_range: int, crit_val: dict) -> dict:
    
    '''
    Function to find the critical area under the curve from the mean of the super-critical area under the curve for the null distribution

    Parameters
    ----------
    null_distribution: dict of the null_distribution values.
    threshold_value: int a range of threshold values graphs were set to.
    permuatation_range: int the range os permuations used.
    crit_val: dict of critical values for each measure.

    Returns
    -------
    null_auc: dict of crticial AUC values for each measure 
    '''
    
    summarized_permutations = summarize_null_distribution(null_distribution, threshold_value, permuatation_range)
    null_auc_results = dict(zip([group for group in summarized_permutations.keys()], [
                    dict() for group in summarized_permutations.keys()]))

    for group_key in null_auc_results.keys():
        for measure in list_of_measures():
            null_auc_results[group_key][measure] = []
            for perm in permuatation_range:
    
                if all(val > 0 for val in summarized_permutations[group_key][measure][perm]) == False and all(val <0 for val in summarized_permutations[group_key][measure][perm]) == False:
                    sum_statistic_list = np.abs(summarized_permutations[group_key][measure][perm])
                    critical = np.abs(crit_val[group_key][measure])
    
                else:
                    sum_statistic_list = summarized_permutations[group_key][measure][perm] 
                    critical = crit_val[group_key][measure]
            
                threshold_values_linspace = np.linspace(start=min(threshold_value), stop=max(threshold_value), num=500)
                observation_interploated = np.interp(threshold_values_linspace, threshold_value, sum_statistic_list)
                observation_interploated -= critical
                
                if  all(val >0 for val in summarized_permutations[group_key][measure][perm]) == True:
                    observation_interploated[observation_interploated<0] = 0
                    
                else:
                    observation_interploated[observation_interploated>0] = 0
    
                obs_AUC = np.trapz(threshold_values_linspace, observation_interploated) 
                null_auc_results[group_key][measure].append(obs_AUC)

    for group_key in null_auc_results.keys():
        for measure in list_of_measures():
            mean = sum(null_auc_results[group_key][measure])/len(permuatation_range)
            null_auc_results[group_key][measure] = mean

    return null_auc_results
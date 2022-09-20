from SCN.folder_structure.folder_utlis import check_path
from SCN.graphs.graph_utlis import load_pickle, save_pickle, list_of_measures
import SCN.graphs.graphs as graphs

import os
import scona as scn
import pandas as pd
from decouple import config
import multiprocessing


def perm_path():
    
    '''
    Function to get permuation pickle file location

    Parameters
    ----------
    None

    Returns
    -------
    file path: str to permutation pickle file
    '''

    return os.path.join(config('root'), 'work/pickle')


def random_graphs(thresholded_graph: scn.BrainNetwork, perms: int, name: str = 'graph') -> dict:
    '''
    Function to simulate random graphs for checking that actual graphs 
    differs from the random graphs. 

    Parameters
    -----------
    thresholded_graph: scona thresholded graph object.
    perms: int, number of permutations
    name: optional str, Name of graph object



    Returns
    ---------
    results: dict, pandas dataframe of global measures, 
             rich club and small world properties.

    '''

    brain_bundle = scn.GraphBundle(
        [thresholded_graph], [f'{name}_thresholded'])
    brain_bundle.create_random_graphs(f'{name}_thresholded', perms)

    global_measures = brain_bundle.report_global_measures()
    rich_club = brain_bundle.report_rich_club()
    small_world = brain_bundle.report_small_world(f'{name}_thresholded')
    small_world_df = pd.DataFrame.from_dict(
        small_world, orient='index', columns=['small_world_coefficient'])

    return {
        'small_world': small_world_df,
        'global_measures': global_measures,
        'rich_club': rich_club,
    }


def random_graph_permutations(thresholded_graph: scn.BrainNetwork, perms: int,  measure: str, name: str = 'graph') -> dict:
    '''
    Function wrapper around random_graphs function. Will pickle results for later use in work/pickle.
    Will load pickle file if exists. 

    Parameters
    --------------------------------------------------
    thresholded_graph: scona thresholded graph object.
    perms: int, number of permutations
    name: optional str, Name of graph object

    Returns
    --------------------------------------------------
    results: dict, pandas dataframe of global measures, 
             rich club and small world properties.

    '''

    pickle_file = f'/assumptions/{measure}_random_graphs_for_{name}_at_{perms}_permutations'
    data_path = os.path.join(perm_path(), 'assumptions')
    file_exist = check_path(os.path.join(data_path, f'{pickle_file}.pickle'))

    if file_exist == False:

        results = random_graphs(thresholded_graph, perms, name)
        save_pickle(pickle_file, results)

    if file_exist == True:

        try:
            results = load_pickle(pickle_file)
            print('\nLoaded previous permutation file\n')

        except Exception:

            print('\nError while loading pickle file. Permutating now\n')
            results = random_graphs(thresholded_graph, perms, name)
            save_pickle(pickle_file, results)

    return results


class Group_permutations:

    '''
    Class to create the null distribution. 

    Usage
    -----
    perm_group = perms.Group_permutations(10, range(4,10))
    perm_group.set_up_data(aan, wr)
    perm_group.create_null_distribution()
    null = perm_group.get_null_distribution()
    perm_group.cleanup()
    '''
    
    def __init__(self, permutation_range: int, threshold_range: int) -> None:

        self.permutation_range = permutation_range
        self.threshold_range = threshold_range
        self.root = config('root')
        self.measures = list_of_measures()

    def set_up_data(self, *data) -> None:

        self.data = dict(zip([f'group_{key}'for key in range(len(data))], [group for group in data]))
        self.groups = len(self.data.keys())

    def null_distro_dict(self) -> dict:
        
        groups = list(self.data.keys())
        null_distro_list = []
        for outergroup in groups:
            for innergroup in groups[::-1]:
                if outergroup != innergroup:
                    check_not_in_list = f'{outergroup}/{innergroup}'
                    if '_'.join(check_not_in_list.split('/')[::-1]) not in null_distro_list:
                         null_distro_list.append(f'{outergroup}_{innergroup}') 
        

        return dict(zip([group for group in null_distro_list], [dict() for group in null_distro_list]))

    def permutations(self, keys) -> dict:

        '''
        Permutations saves the dictionary files to the pickle directory. 
        '''
        
        null_distribution ={
    
            'average_clustering':[],
            'average_shortest_path_length':[], 
            'assortativity':[], 
            'modularity':[], 
            'efficiency':[],
            'small_world':[]
        }
        
        centroids = graphs.load_centroids()
        names = graphs.load_names()
        group1 = self.data[keys[0]]
        group2 = self.data[keys[1]]
        participants = pd.concat([group1, group2])
        
        print(f'\nCreating null distribution for groups {keys[0]} and {keys[1]} thresholded at {keys[2]}')
        for perm in range(self.permutation_range):
            group_1 = participants.sample(n=group1.shape[0])
            group_2 = participants.sample(n=group2.shape[1])
    
            group1_graphs = graphs.create_graphs(group_1, names, centroids, keys[2])
            group2_graphs = graphs.create_graphs(group_2, names, centroids, keys[2])
    
            group_1_values = group1_graphs['graph_threshold'].calculate_global_measures()
            group_2_values = group2_graphs['graph_threshold'].calculate_global_measures()
    
            for meas in self.measures:
                crit_val = group_1_values[meas] - group_2_values[meas]
                null_distribution[meas].append(crit_val)
        
        
        save_pickle(f'group_differences/tmp_null_distribution/{keys[0]}_{keys[1]}_thresholded_value_{keys[2]}_null_distribution', null_distribution)
    
    def create_null_distribution(self):
        
        os.mkdir(f'{self.root}/work/pickle/group_differences/tmp_null_distribution')
        
        for threshold in self.threshold_range: 

            if self.groups == 2:
                null_distribution_values = self.permutations(['group_0', 'group_1', threshold]) 
            
            if self.groups == 3:
                
                group0_group1_null_distribution_values = multiprocessing.Process(target=self.permutations, args=(['group_0', 'group_1', threshold], ))
                group0_group2_null_distribution_values = multiprocessing.Process(target=self.permutations, args=(['group_0', 'group_2', threshold], ))
                group1_group2_null_distribution_values = multiprocessing.Process(target=self.permutations, args=(['group_1', 'group_2', threshold], ))
              
                group0_group1_null_distribution_values.start()
                group0_group2_null_distribution_values.start()
                group1_group2_null_distribution_values.start()

                group0_group1_null_distribution_values.join()
                group0_group2_null_distribution_values.join()
                group1_group2_null_distribution_values.join()

                print('\nExit code for group_0 and group_1 null distribution is ', group0_group1_null_distribution_values.exitcode)
                print('\nExit code for group_0 and group_2 null distribution is ', group0_group2_null_distribution_values.exitcode)
                print('\nExit code for group_0 and group_3 null distribution is ', group1_group2_null_distribution_values.exitcode)

    def get_null_distribution(self):
        
        import re
        null_distribution = self.null_distro_dict()
        files = os.listdir(os.path.join(config('root'), 'work/pickle/group_differences/tmp_null_distribution'))
        
        threshold = re.compile(r'group_._group_._|_null_distribution')
        for file in files:
            file = re.sub('.pickle', '', file)
            loaded_file = load_pickle('group_differences/tmp_null_distribution/' + file)
            group_key = re.sub(r'_thresholded.*','', file)
            threshold_key = re.sub(threshold, '', file)
            null_distribution[group_key][threshold_key] = loaded_file

        return null_distribution

    def cleanup(self):
        
        import shutil
        shutil.rmtree(os.path.join(config('root'), 'work/pickle/group_differences/tmp_null_distribution'))
            
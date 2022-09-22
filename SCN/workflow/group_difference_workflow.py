from SCN.group_differences.group_differences import Create_thresholded_graphs, Test_statstic, maximum_null_stat, critical_value, identify_clusters
from SCN.graphs.permutations import Group_permutations
from SCN.graphs.graph_utlis import load_pickle, save_pickle
from SCN.folder_structure.folder_utlis import check_pickle_file

import pandas as pd


def main_group_differences_workflow(group_0: pd.DataFrame, group_1: pd.DataFrame, group_2, perm: int, measure: str, threshold: int) -> bool:

    threshold_range = range(4, threshold)
    perm_range = range(0, perm)
    check_global_measures_exist = check_pickle_file(
        f'group_differences/group_measures_for_{measure}.pickle')

    if check_global_measures_exist == False:
        if type(group_2) == pd.DataFrame:
            graphs = Create_thresholded_graphs(
                threshold_range, group_0, group_1, group_2)
        else:
            graphs = Create_thresholded_graphs(
                threshold_range, group_0, group_1)

        graphs.create()
        group_measures = graphs.global_measures()
        print(f'\nSaving global group measures for {measure} to work/pickle/group_differences')
        save_pickle(
            f'/group_differences/group_measures_for_{measure}', group_measures)

    if check_global_measures_exist == True:
        print('Existing global measures file found. Loading previous file.')
        group_measures = load_pickle(
            f'/group_differences/group_measures_for_{measure}')

    check_test_stats_exist = check_pickle_file(
        f'group_differences/test_stats_for_{measure}.pickle')

    if check_test_stats_exist == False:
        print('\nCalculating difference between measures for each group at each threshold.')
        stats = Test_statstic(group_measures)
        test_stats = stats.test_statistic(threshold_range)
        print('Saving test_statistics')
        save_pickle(f'group_differences/test_stats_for_{measure}', test_stats)

    if check_test_stats_exist == True:
        print('Existing test statistics file found. Loading previous file.')
        test_stats = load_pickle(
            f'/group_differences/test_stats_for_{measure}')

    check_null_distro_exist = check_pickle_file(
        f'group_differences/null_distribution_for_{measure}_at_{perm}_permutations.pickle')

    if check_null_distro_exist == False:
        print('\nCreating the null distribution. WARINING this can takes a long time depending on the number of permuations set')
        print('-'*100)
        perm_group = Group_permutations(perm, threshold_range)

        if type(group_2) == pd.DataFrame:
            perm_group.set_up_data(group_0, group_1, group_2)
        else:
            perm_group.set_up_data(group_0, group_1)

        perm_group.create_null_distribution()
        null_distro = perm_group.get_null_distribution()
        print('\nSaving the null distribution to work/pickle/group_differences and cleaning up tmp files.')
        save_pickle(
            f'group_differences/null_distribution_for_{measure}_at_{perm}_permutations', null_distro)
        perm_group.cleanup()

    if check_null_distro_exist == True:
        print('Existing null distribution file found. Loading previous file.')
        null_distro = load_pickle(
            f'/group_differences/null_distribution_for_{measure}_at_{perm}_permutations')
    
    check_max_exists = check_pickle_file(
        f'group_differences/maxi_null_statistic_for_{measure}_at_{perm}_permutations.pickle')

    if check_max_exists == False:
        print('\nCalculating the maximum test statistic for each permuation across all thresholds.')
        maxi_null_statistic = maximum_null_stat(
            null_distro, threshold_range, perm_range)
        print('Saving maximum null statistic')
        save_pickle(f'group_differences/maxi_null_statistic_for_{measure}_at_{perm}_permutations', maxi_null_statistic)
    
    if check_max_exists == True:
        print('Existing maximum null statistic file found. Loading previous file.')
        maxi_null_statistic = load_pickle(
           f'group_differences/maxi_null_statistic_for_{measure}_at_{perm}_permutations')

    print('Calculating critical values for the test-statistics from the maximum null distribution')
    crit_values = critical_value(maxi_null_statistic)
    
    print('Idenitifying clusters where test-statistic is greater than the critical value.')
    clusters = identify_clusters(test_stats, crit_values, maxi_null_statistic)
    
    if len(clusters) == 0:
        print('No significant clusters found. Exiting')
        return False

    if len(clusters) != 0:
        print('\nThe following clusters reach are above the threshold:\n')
        print(*clusters.keys(), sep='\n')
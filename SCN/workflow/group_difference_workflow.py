from SCN.group_differences.group_differences import Create_thresholded_graphs, Test_statstic, maximum_null_stat
from SCN.graphs.permutations import Group_permutations
from SCN.graphs.graph_utlis import save_pickle
import pandas as pd


def main_group_differences_workflow(group_0: pd.DataFrame, group_1: pd.DataFrame,  group_2, perm: int, measure: str, threshold: int) -> None:
    
    threshold_range = range(4, threshold)
    perm_range = range(0, perm)
    
    if type(group_2) == pd.DataFrame:
        graphs = Create_thresholded_graphs(threshold_range, group_0, group_1, group_2)
    else:
        graphs = Create_thresholded_graphs(threshold_range, group_0, group_1)
    
    graphs.create()
    group_measures = graphs.global_measures()
    print(f'\nSaving global group measures for {measure} to work/pickle/group_differences')
    save_pickle(f'/group_differences/group_measures_for_{measure}', group_measures)

    print('\nCalculating difference between measures for each group at each threshold.')
    stats = Test_statstic(group_measures)
    test_stats = stats.test_statistic(threshold_range)
    save_pickle(f'group_differences/test_stats_for_{measure}', test_stats)

    print('\nCreating the null distribution. WARINING this can takes a long time depending on the number of permuations set')
    print('-'*75)
    perm_group = Group_permutations(perm, threshold_range)

    if type(group_2) == pd.DataFrame:
        perm_group.set_up_data(group_0, group_1, group_2)
    else:
        perm_group.set_up_data(group_0, group_1)
    
    perm_group.create_null_distribution()
    null = perm_group.get_null_distribution()

    print('\nSaving the null distribution to work/pickle/group_differences and cleaning up tmp files.')
    
    save_pickle(f'group_differences/null_distribution_for_{measure}_at_{perm}_permutations', null)
    perm_group.cleanup()
    
    print('\nCalculating the maximum test statistic for each permuation across all thresholds.')
    maxi_null_statistic = maximum_null_stat(null, threshold_range, perm_range )
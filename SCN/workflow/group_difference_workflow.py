from SCN.group_differences import Create_thresholded_graphs, Test_statstic
import pandas as pd


def main_group_differences_workflow(group_0: pd.DataFrame, group_1: pd.DataFrame,  group_2, perm: int, measure: str, threshold: int) -> None:
    
    threshold_range = range(4, threshold)
    
    graphs = Create_thresholded_graphs(range(4,100), aan, wr, hc)
    graphs.create()
    measures = graphs.global_measures()
     
     
    stats = Test_statstic(measures)
    test_stats = stats.test_statistic(range(4,100))
    save_pickle('group_differences/test_stats', test_stats)
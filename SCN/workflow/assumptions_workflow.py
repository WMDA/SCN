from SCN.graphs.graph_utlis import load_pickle
from SCN.graphs.graphs import create_graphs, load_names, load_centroids
from SCN.assumptions.random_graph_creation import Random_Graph_Creator
from SCN.assumptions.visual_graphs import distro_plots, network_measures_plot
from SCN.assumptions.create_html_view import HTML_file
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def main_assumptions_work_flow(group_0: pd.DataFrame, group_1: pd.DataFrame,  group_2, perm, measure):

    names = load_names()
    centroids = load_centroids()
    random_graphs = Random_Graph_Creator(perm, measure)

    group_0 = create_graphs(group_0, names, centroids, threshold=10)
    group_1 = create_graphs(group_1, names, centroids, threshold=10)

    if type(group_2) == pd.DataFrame:
        group_2 = create_graphs(group_2, names, centroids, threshold=10)
        random_graphs.setup_data(
            group_0['graph_threshold'], group_1['graph_threshold'], group_2['graph_threshold'])

    else:
        random_graphs.setup_data(
            group_0['graph_threshold'], group_1['graph_threshold'])

    random_graphs.permutations()

    print('\nCreating Graphs for network measures and distribution plots\n')
    group_0_pickled = load_pickle(
        f'/assumptions/{measure}_random_graphs_for_group_0_at_{perm}_permutations')
    distro_plots(group_0_pickled['global_measures'], 'group_0')
    network_measures_plot(group_0_pickled, 'group_0_thresholded', 'group_0')
    group_0_plot = HTML_file('group_0')
    group_0_plot.save_to_file()

    group_1_pickled = load_pickle(
        f'/assumptions/{measure}_random_graphs_for_group_1_at_{perm}_permutations')
    distro_plots(group_1_pickled['global_measures'], 'group_1')
    network_measures_plot(group_1_pickled, 'group_1_thresholded', 'group_1')
    group_1_plot = HTML_file('group_1')
    group_1_plot.save_to_file()

    try:
        group_2_pickled = load_pickle(
            f'/assumptions/{measure}_random_graphs_for_group_2_at_{perm}_permutations')
        distro_plots(group_2_pickled['global_measures'], 'group_2')
        network_measures_plot(
            group_2_pickled, 'group_2_thresholded', 'group_2')
        group_2_plot = HTML_file('group_2')
        group_2_plot.save_to_file()

    except Exception:
        print('\nWarnings about loading pickle files for group 2 can safely be ignored.')

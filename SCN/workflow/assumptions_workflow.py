'''
workflow 
- Work out number of groups X
- create graphs for each group X
- create random graphs 
- graph output 

'''


from SCN.graphs.graphs import create_graphs, load_names, load_centroids
from SCN.assumptions.random_graph_creation import Random_Graph_Creator
from SCN.assumptions.visual_graphs import distro_plots, network_measures_plot
from SCN.assumptions.create_html_view import HTML_file
import pandas as pd
from decouple import config



def main_assumptions_work_flow(group_0: pd.DataFrame, group_1: pd.DataFrame, perm, group_2: bool = False):

    names = load_names()
    centroids = load_centroids()

    group_0 = create_graphs(group_0, names, centroids, threshold=10)
    group_1 = create_graphs(group_1, names, centroids, threshold=10)

    if group_2 != False:
        group_2 = create_graphs(group_2, names, centroids, threshold=10)


    random_graphs = Random_Graph_Creator(perm)
    random_graphs.setup_data(group_0['graph_threshold'], group_1['graph_threshold'], group_2['graph_threshold'])
    random_graphs.permutations()
    HTML_file


# External modules
import os
from decouple import config
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('dark')

# scn modules
from SCN.graphs.graph_utlis import df_for_sns_barplot, list_of_measures

def graph_directory() -> str:
    '''
    Function to return abosulte path of graphs working directory.

    Pararmeters
    ----------
    None

    Returns
    -------
    str: abosulte path of graph working directory
    '''
    return os.path.join(config('root'), 'work/visual_graphs')


def distro_plots(data: pd.DataFrame, name: str, structural_measure: str) -> None:
    '''
    Plots the distibution of clustering, 
    shortest_path, assortativity, modularity and efficiency. 

    Parameters
    ----------
    data: pandas df from the output of report_global_measures() from scona package
    name: str name to call file

    Returns
    -------
    None

    '''

    fig, ax = plt.subplots(1, 5, figsize=(35, 8))
    sns.histplot(data=data, x='average_clustering',
                 color='darkorange', ax=ax[0])
    sns.histplot(data=data, x='average_shortest_path_length',
                 color='purple', ax=ax[1])
    sns.histplot(data=data, x='assortativity', color='darkblue', ax=ax[2])
    sns.histplot(data=data, x='modularity', color='red', ax=ax[3])
    sns.histplot(data=data, x='efficiency', ax=ax[4])

    directory = graph_directory()
    fig.savefig(f'{directory}/distro_plots_for_{name}_for_{structural_measure}.png')


def network_measures_plot(brain_bundle, original_network: str, name: str, structural_measure: str) -> None:
    """
    Modified scona function plot_network_measures. See original for full documentation.
    Main difference is it calls df_for_sns_barplot rather than create_df_sns_barplot
    """

    sns.set_context("poster", font_scale=1)
    seaborn_data = df_for_sns_barplot(brain_bundle, original_network)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(x="measure", y="value", hue="TypeNetwork",
                     data=seaborn_data, palette=['purple', 'slategrey'], ci=95)

    ax.axhline(0, linewidth=0.8, color='black')
    ax.set_ylabel("Global network measures")
    ax.set_xlabel("")
    ax.legend(fontsize="xx-small")

    sns.despine()
    plt.tight_layout()
    directory = graph_directory()
    plt.savefig(f'{directory}/network_measures_plot_for_{name}_for_{structural_measure}.png')

def cluster_plots(test_statistics: dict, crit: dict, group: str, structural_measure: str ) -> None:
    
    '''
    Function to create a save cluster plots.

    Parameters
    ----------
    test_statistics: dict of test_stats
    crit: dict of critical values
    group: str of name of groups.
    structural_measure : str of structural measure being examined

    Returns
    -------
    None
    '''

    fig, ax = plt.subplots(1, 5,figsize=(25, 5))
    for index, measure in enumerate(list_of_measures()):
        df = pd.DataFrame([list(range(4,101)), test_statistics[group][measure]]).T.rename(columns={0:'threshold', 1:'test_stat'})
        graph = sns.lineplot(y ='test_stat', x='threshold', data=df.abs(), ax=ax[index])
        graph.axhline(crit[group][measure])
        graph.set(xlabel='Thresholds',
                  ylabel='Test statistics',
                  title=measure)
  
    directory = graph_directory()
    plt.savefig(f'{directory}/cluster_plots_for_{group}_for_{structural_measure}.png')
    
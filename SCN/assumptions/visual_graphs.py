#External modules
import os
from decouple import config
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('dark')

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


def distro_plots(data:pd.DataFrame, name: str) -> None:
    
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

    fig, ax = plt.subplots(1,5, figsize=(35,8))
    sns.histplot(data=data, x='average_clustering', color='darkorange', ax=ax[0])
    sns.histplot(data=data, x='average_shortest_path_length', color='purple', ax=ax[1])
    sns.histplot(data=data, x='assortativity', color='darkblue', ax=ax[2])
    sns.histplot(data=data, x='modularity',color='red', ax=ax[3])
    sns.histplot(data=data, x='efficiency', ax=ax[4])
 
    directory = graph_directory()
    fig.savefig(f'{directory}/{name}.png')

def df_for_sns_barplot(measures, original_network) -> pd.DataFrame:
    
    '''
    modified scona create_df_sns_barplot function.
    See original function for full documentation.
    
    Main difference is this function does not calculate global and small world measures 
    as this has been done by previous functions. 

    Also refactored code to remove unecessary variables.
    '''
    
    bundleGraphs_measures = measures['global_measures']
    small_world = measures['small_world']

    abbreviation = {'assortativity': 'a',
                    'average_clustering': 'C',
                    'average_shortest_path_length': 'L',
                    'efficiency': 'E',
                    'modularity': 'M'}

    new_columns = ["measure", "value", "TypeNetwork"]
    no_columns_old = len(bundleGraphs_measures.columns)
    no_rows_old = len(bundleGraphs_measures.index)
    total_rows = no_columns_old * no_rows_old
    index = [i for i in range(1, total_rows + 1)]
    data_array = list()

    for measure in bundleGraphs_measures.columns:
 
        try:
            value = bundleGraphs_measures.loc[original_network, measure]
        except Exception as e:
            print(e)

        measure_short = abbreviation[measure]
        tmp = [measure_short, value, "Observed network"]
        data_array.append(tmp)

    random_df = bundleGraphs_measures.drop(original_network)

    for measure in random_df.columns:

        for rand_graph in random_df.index:
            value = random_df[measure][rand_graph]
            measure_short = abbreviation[measure]
            tmp = [measure_short, value, "Random network"]
            data_array.append(tmp)


    NewDataFrame = pd.DataFrame(data=data_array, index=index,
                                columns=new_columns)

    if len(small_world) > 1:

        df_small_world = []
        for i in small_world.values:
            tmp = {'measure': 'sigma',
                   'value': float(i),
                   'TypeNetwork': 'Observed network'}

            df_small_world.append(tmp)

        NewDataFrame = NewDataFrame.append(df_small_world, ignore_index=True)

        rand_small_world = {'measure': 'sigma',
                            'value': 1,
                            'TypeNetwork': 'Random network'}

        NewDataFrame = NewDataFrame.append(rand_small_world,
                                           ignore_index=True)

    return NewDataFrame


def network_measures_plot(brain_bundle, original_network: str, name: str) -> None:
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
    plt.savefig(f'{directory}/{name}.png')

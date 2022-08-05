'''
A script of modified scona functions to accomadate changes in how metrics are calculated. 
'''
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

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


def network_measures_plot(brain_bundle, original_network, color:str=None, ci:int=95, show_legend:bool=True):
    """
    Modified scona function plot_network_measures. See original for full documentation.
    Main difference is it calls df_for_sns_barplot rather than create_df_sns_barplot
    """

    sns.set_context("poster", font_scale=1)
    seaborn_data = df_for_sns_barplot(brain_bundle, original_network)

    if color is None:
        color = [sns.color_palette()[0], "lightgrey"]
    elif len(color) == 1:           
        color.append("lightgrey")

    if not isinstance(color, list) and len(color) != 2:
        warnings.warn("Please, provide a *color* parameter as a "
                      "python list object, e.g. [\"green\", \"pink\"]. "
                      "Right now the default colors will be used")
        color = [sns.color_palette()[0], "lightgrey"]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(x="measure", y="value", hue="TypeNetwork",
                     data=seaborn_data, palette=[color[0], color[1]], ci=ci)

    ax.axhline(0, linewidth=0.8, color='black')
    ax.set_ylabel("Global network measures")
    ax.set_xlabel("")  

    if show_legend:
        ax.legend(fontsize="xx-small")
    else:
        ax.legend_.remove()

    sns.despine()
    plt.tight_layout()
    plt.show()

def rich_club_plot(brain_bundle, original_network, color=None, show_legend=True, x_max=None, y_max=None):

    '''
    Modified scona function plot_rich_club. See original function for full details.

    Main difference is doesn't calculate rich club as another function does this.
    '''
    
    sns.set_context("poster", font_scale=1)
    rich_club_df = brain_bundle['rich_club']
    degree = rich_club_df.index.values

    try:
        rc_orig = np.array(rich_club_df[original_network])
    except KeyError:
        raise KeyError("Please check the name of the initial Graph (the proper network, the one you got from the mri data) in GraphBundle. There is no graph keyed by name \"{original_network}\"")

    rand_df = rich_club_df.drop(original_network, axis=1)
    rand_degree = []
    rc_rand = []
    for i in range(len(rand_df.columns)):
        rand_degree = np.append(rand_degree, rand_df.index.values)
        rc_rand = np.append(rc_rand, rand_df.iloc[:, i])

    new_rand_df = pd.DataFrame({'Degree': rand_degree, 'Rich Club': rc_rand})
    fig, ax = plt.subplots(figsize=(10, 6))

    if color is None:
        color = ["#00C9FF", "grey"]
    elif len(color) == 1:             
        color.append("grey")           

    if not isinstance(color, list) and len(color) != 2:
        warnings.warn("Please, provide a *color* parameter as a "
                      "python list object, e.g. [\"green\", \"pink\"]. "
                      "Right now the default colors will be used")
        color = ["#00C9FF", "grey"]

    ax = sns.lineplot(x=degree, y=rc_orig, label="Observed network", zorder=1,
                      color=color[0])

    ax = sns.lineplot(x="Degree", y="Rich Club", data=new_rand_df,
                      err_style="band", ci=95, color=color[1],
                      label="Random network", zorder=2)

    if x_max is None:
        x_max = max(degree)

    if y_max is None:
        y_max = max(rc_orig) + 0.1  

    ax.set_xlim((0, x_max))
    ax.set_ylim((0, y_max))
    ax.locator_params(nbins=4)
    ax.set_xlabel("Degree")
    ax.set_ylabel("Rich Club")

    if show_legend:
        ax.legend(fontsize="x-small")
    else:
        ax.legend_.remove()

    sns.despine()
    plt.tight_layout()
    plt.show()
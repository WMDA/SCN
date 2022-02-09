'''
Functions to plot graph measures
'''

#External modules
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')

#SCN modules
import functions.statistical_functions as Sfun

def distro_plots(data):
    
    '''
    Wrapper function around sns.histplots to plot the distibution of clustering, 
    shortest_path, assortativity, modularity and efficiency.

    Parameters
    ------------------------------------------------------------------------------
    data: pandas df from the output of report_global_measures() from scona package

    Returns
    -------------------------------------------------------------------------
    plots: 5x1 grid of histplots for clustering, shortest_path, assortativity,
           modularity and efficiency
    '''

    fig, ax = plt.subplots(1,5, figsize=(35,8))
    sns.histplot(data=data, x='average_clustering', color='darkorange', ax=ax[0])
    sns.histplot(data=data, x='average_shortest_path_length', color='purple', ax=ax[1])
    sns.histplot(data=data, x='assortativity', color='darkblue', ax=ax[2])
    sns.histplot(data=data, x='modularity',color='red', ax=ax[3])
    sns.histplot(data=data, x='efficiency', ax=ax[4])
    plt.show()


def pval_plotting(ctvalues, tcrit_value, measure, permutations):
    
    '''
    Wrapper around seaborn displot.
    Function to plot null distribution with 2 std either side and true critical value.

    Parameters
    -----------------------------------------------------------------
    ctvalues : list, list of crticial values from the null distrubtion.
    tcrit_value: int True crtical value of a test.
    measure: str, name of the measure (used in title of the graph)
    permutations: int, number of permuations (used in title of the graph)


    Returns
    -----------------------------------------------------------------
    hist: histogram of null distribution with upper and lower std with
          true value.
    '''
    
    #Calculates the mean and std deviation of null distribution

    mean_val = Sfun.mean_std(ctvalues)
    
    #plots 
    hist = sns.displot(data=ctvalues, height=10).set(title=f'Histplot for {measure} after {permutations} permuatations')
    hist.refline(x=tcrit_value, color='purple')
    hist.refline(x=mean_val['lower_2std'], linestyle='-', color='black')
    hist.refline(x=mean_val['upper_2std'], linestyle='-', color='black')
    hist.refline(x=mean_val['lower_1std'], linestyle='-', color='red')
    hist.refline(x=mean_val['upper_1std'], linestyle='-', color='red')
    plt.show()

def create_df_sns_barplot(bundleGraphs, original_network):


    # calculate network measures for each graph in brain_bundle
    # if each graph in GraphBundle has already calculated global measures,
    # this step will be skipped
    bundleGraphs_measures = bundleGraphs

    # set abbreviations for measures
    abbreviation = {'assortativity': 'a',
                    'average_clustering': 'C',
                    'average_shortest_path_length': 'L',
                    'efficiency': 'E',
                    'modularity': 'M'}

    # set columns for our new DataFrame
    new_columns = ["measure", "value", "TypeNetwork"]

    # get the number of columns from the old DataFrame
    no_columns_old = len(bundleGraphs_measures.columns)

    # get the number of rows from the old DataFrame
    no_rows_old = len(bundleGraphs_measures.index)

    # set number of rows (indexes) in new DataFrame
    total_rows = no_columns_old * no_rows_old

    # set index for our new DataFrame
    index = [i for i in range(1, total_rows + 1)]

    # Build array to contain all data to futher use for creating new DataFrame

    # store values of *Real Graph* in data_array - used to create new DataFrame
    data_array = list()

    for measure in bundleGraphs_measures.columns:
        # check that the param - original_network - is correct,
        # otherwise pass an error
        try:
            # for original_network get value of each measure
            value = bundleGraphs_measures.loc[original_network, measure]
        except KeyError:
            raise KeyError(
                "The name of the initial Graph you passed to the function - \"{}\""              # noqa
                " does not exist in GraphBundle. Please provide a true name of "
                "initial Graph (represented as a key in GraphBundle)".format(original_network))  # noqa

        # get the abbreviation for measure and use this abbreviation
        measure_short = abbreviation[measure]

        type_network = "Observed network"

        # create a temporary array to store measure - value of Real Network
        tmp = [measure_short, value, type_network]

        # add the record (measure - value - Real Graph) to the data_array
        data_array.append(tmp)

    # now store the measure and measure values of *Random Graphs* in data_array

    # delete Real Graph from old DataFrame -
    random_df = bundleGraphs_measures.drop(original_network)

    # for each measure in measures
    for measure in random_df.columns:

        # for each graph in Random Graphs
        for rand_graph in random_df.index:
            # get the value of a measure for a random Graph
            value = random_df[measure][rand_graph]

            # get the abbreviation for measure and use this abbreviation
            measure_short = abbreviation[measure]

            type_network = "Random network"

            # create temporary array to store measure - value of Random Network
            tmp = [measure_short, value, type_network]

            # add record (measure - value - Random Graph) to the global array
            data_array.append(tmp)

    # finally create a new DataFrame
    NewDataFrame = pd.DataFrame(data=data_array, index=index,
                                columns=new_columns)

    # include the small world coefficient into new DataFrame

    # check that random graphs exist in GraphBundle
    if len(bundleGraphs) > 1:
        # get the small_world values for Real Graph
        small_world = bundleGraphs.report_small_world(original_network)

        # delete the comparison of the graph labelled original_network with itself  # noqa
        del small_world[original_network]

        # create list of dictionaries to later append to the new DataFrame
        df_small_world = []
        for i in list(small_world.values()):
            tmp = {'measure': 'sigma',
                   'value': i,
                   'TypeNetwork': 'Observed network'}

            df_small_world.append(tmp)

        # add small_world values of *original_network* to new DataFrame
        NewDataFrame = NewDataFrame.append(df_small_world, ignore_index=True)

        # bar for small_world measure of random graphs should be set exactly to 1   # noqa

        # set constant value of small_world measure for random bar
        rand_small_world = {'measure': 'sigma',
                            'value': 1,
                            'TypeNetwork': 'Random network'}

        # add constant value of small_world measure for random bar to new DataFrame # noqa
        NewDataFrame = NewDataFrame.append(rand_small_world,
                                           ignore_index=True)

    return NewDataFrame

def plot_network_measures(brain_bundle, original_network, color=None, ci=95, show_legend=True):
   
    sns.set_context("poster", font_scale=1)

    # build a new DataFrame required for seaborn.barplot
    seaborn_data = create_df_sns_barplot(brain_bundle, original_network)

    # set the default colors of barplot values if not provided
   
    if color is None:
        color = [sns.color_palette()[0], "lightgrey"]
    elif len(color) == 1:            # in case we want to plot only real values
        color.append("lightgrey")

    # if the user provided color not as a list of size 2 - show warning
    # use default colors
    if not isinstance(color, list) and len(color) != 2:
        print("Please, provide a *color* parameter as a "
                      "python list object, e.g. [\"green\", \"pink\"]. "
                      "Right now the default colors will be used")
        color = [sns.color_palette()[0], "lightgrey"]

    # Create a figure
    fig, ax = plt.subplots(figsize=(8, 6))

    # plot global measures with error bars
    ax = sns.barplot(x="measure", y="value", hue="TypeNetwork",
                     data=seaborn_data, palette=[color[0], color[1]], ci=ci)

    # make a line at y=0
    ax.axhline(0, linewidth=0.8, color='black')

    # set labels for y axix
    ax.set_ylabel("Global network measures")
    ax.set_xlabel("")   # empty -> no x-label

    # create a legend if show_legend = True, otherwise - remove
    if show_legend:
        ax.legend(fontsize="xx-small")
    else:
        ax.legend_.remove()

    # remove the top and right spines from plot
    sns.despine()

    # adjust subplot params so that the subplot fits in to the figure area
    plt.tight_layout()

    # display the figure
    plt.show()
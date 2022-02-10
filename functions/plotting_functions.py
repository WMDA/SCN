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
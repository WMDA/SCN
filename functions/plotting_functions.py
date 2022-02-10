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
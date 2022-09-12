#External modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('dark')


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
    fig.savefig(f'{name}.png')
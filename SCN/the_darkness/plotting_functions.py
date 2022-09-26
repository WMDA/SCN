'''
Functions to plot graph measures
'''

#External modules
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set_style('dark')

#SCN modules
import functions.statistical_functions as Sfun



def pval_plotting(ctvalues:list, tcrit_value:int, measure:str, permutations:int) -> None:
    
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
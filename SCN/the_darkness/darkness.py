import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('dark')



def rich_club_plot(brain_bundle, original_network, color=None, show_legend=True, x_max=None, y_max=None) -> None:

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
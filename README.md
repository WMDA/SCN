# SCN

SCN is a structural covariance network pipeline built in python. It uses the scona package as a basis for building the graphs then use the methodology out line by Drakesmith to permutate for group differences in global measures. 

Current time SCN can't calculate or permuate group differences for nodal measures only global measure. Hopefully in future releases this functionality can be added.

## Usage

```
usage: SCN [-h] [-g0 GROUP_0] [-g1 GROUP_1] [-g2 GROUP_2] [-p PERMS] [--path PATH] [-n NAME]
           [-s] [-w WDIR] [-m MEASURE] [-G] [-N] [-t THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  -g0 GROUP_0, --group_0 GROUP_0
                        csv file of participants structural measures. SCN at the moment does
                        not track group names only numbers. SCN also can only handle upto
                        three groups.
  -g1 GROUP_1, --group_1 GROUP_1
                        csv file of participants structural measures. SCN at the moment does
                        not track group names only numbers. SCN also can only handle upto
                        three groups.
  -g2 GROUP_2, --group_2 GROUP_2
                        csv file of participants structural measures. SCN at the moment does
                        not track group names only numbers. SCN also can only handle upto
                        three groups.
  -p PERMS, --perms PERMS
                        number of permuations to do
  --path PATH           filepath to set up project in
  -n NAME, --name NAME  name of project. Default is SCN
  -s, --skip            skip folder set up
  -w WDIR, --wdir WDIR  working directory where data is stored
  -m MEASURE, --measure MEASURE
                        measure that is being examined
  -G, --group-only      Run only group differences. Skips assumptions workflow
  -N, --no-logs         Does not store output in log files.
  -t THRESHOLD, --threshold THRESHOLD
                        Upper boundary to threshold graphs at. Default is set at 99.
```

SCN sets up a folder structure like this:

```
SCN
├── logs
│   └── log files go here
│   
├── results
│   ├── assumptions
|   |   └── html file for group assumptions go here      
│   └── group_differences
│       ├── global measure csvs for each structural measure go here
│       └── html file for group differences go here 
└── work
    ├── pickle
    │   ├── assumptions
    │   │   └── random graphs permuation pickle file for each group goes here
    │   └── group_differences
    │       ├── pickle file for group_measures
    │       ├── pickle file maximum null statistics for a structural measure at a set number of permutations
    │       ├── pickle file for null distribution 
    │       └── pickle file for test stats 
    └── visual_graphs
        ├── png for cluster_plots for each group
        ├── png for distro plots for each group 
        ├── png for global_measure plots for
        └── png for network measures plots for each group


```

## References

Drakesmith, M., Caeyenberghs, K., Dutt, A., Lewis, G., David, A., & Jones, D. (2015). Overcoming the effects of false positives and threshold bias in graph theoretical analyses of neuroimaging data. Neuroimage, 118, 313-333. doi: 10.1016/j.neuroimage.2015.05.011

Scona package can be found at https://github.com/WhitakerLab/scona
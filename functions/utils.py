import time

class TimeError(Exception):
    """Custom Timer Exception"""

class Timer:

    def __init__(self):
        self.__start = None

    def start(self):
        if self.__start is not None:
            raise TimeError("Timer is already started")

        self.__start = time.perf_counter()

    def stop(self):
        if self.__start is None:
            raise TimeError("Timer has not been started. Use .start() to start timer")
        
        time_taken = time.perf_counter() - self.__start
        self.__start = None
        print(f"Finished in {time_taken} seconds")









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
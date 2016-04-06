import pandas as pd


class DataAggregator:
    def __init__(self, window_size=5):
        self.window_size = window_size

    def read(self, filepath):
        """
        Generates the aggregated data. For each day there is the average mood (the value) and the features.
        There are a few possiible variables. For each variable we take the sum and the average over each day. These
        Will be the features.
        :param filepath:
        :return:
        """

        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        df = pd.read_csv(filepath, parse_dates=['time'], date_parser=dateparse)
        print df.keys()
        participants = df['id'].unique()  # all participants (don't know if needed)
        vars = df['variable'].unique()  # all possible variables

        current_date = pd.datetime(2014, 4, 3)  # is set on midnigth, the start of the day.
        start_date = current_date - pd.DateOffset(days=5)
        end_date = current_date
        print current_date, start_date, end_date
        # a query on the date range, for a specific pariticipant.
        mask = (df['time'] > start_date) & (df['time'] <= end_date) & (df['id'] == 'AS14.01')
        # apply query
        tf = df.loc[mask]

        # group by day
        gs = tf.groupby(pd.TimeGrouper(key='time', freq='D'))
        for g in gs:
            # g is a tuple, g[0] is the how the group is created, g[1] is the dataframe
            gdf = g[1]
            for var in vars:
                varselection = gdf.loc[(gdf['variable'] == var)]
                daymean = varselection['value'].mean()
                daysum = varselection['value'].sum()
                dayvar = varselection['value'].var() #variance
                print var, daymean, daysum, dayvar
                # print gdf.loc[(gdf['variable'] == var)]
                # print g[1]['value'].mean()
            break

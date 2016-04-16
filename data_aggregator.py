import pandas as pd

import numpy as np


class DataAggregator:
    def __init__(self, filepath, window_size=5, variables=None):
        self.window_size = window_size
        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        self.df = pd.read_csv(filepath, parse_dates=['time'], index_col='time', date_parser=dateparse)
        self.participants = self.df['id'].unique()  # all participants (don't know if needed)
        if variables:
            self.variables = variables
        else:
            self.variables = self.df['variable'].unique()  # all possible variables
        print "data opened"

    def read(self, method='separate'):
        """
        Generates the aggregated data. For each day there is the average mood (the value) and the features.
        There are a few possible variables. For each variable we take the sum and the average over each day. These
        Will be the features.
        :param filepath:
        :return:
        """
        

        if method == 'combined':
            return self.window_combined_days(self.window_size)
        elif method == 'separate':
            return self.window_separate_days(self.window_size)
        elif method == 'all':
            return self.all_data()

    def all_data(self):
        moods = []
        index_dates = []
        current_id = self.participants[0]
        mask = (self.df['id'] == current_id)

        # get every date for one person
        tf = self.df.loc[mask]
        tf = tf.ix[pd.to_datetime(tf.index).sort_values()]
        dates = np.unique(np.array(tf.index.map(pd.Timestamp.date)))
        for date in dates:
            end = date
            cur_day = tf[end:end + pd.DateOffset(days=1)]
            mood_selection = cur_day.loc[(cur_day['variable'] == 'mood')]
            if len(mood_selection) > 0:
                mood_mean = mood_selection['value'].mean()
            moods.append(mood_mean)
            index_dates.append(date)
        return pd.DataFrame(moods, index=pd.DatetimeIndex(index_dates), columns=['Mood'])

    def window_separate_days(self, window_size):
        #Shouldnt we set this date to the last day that this person filled in the form on his telephone?
        current_date = pd.datetime(2014, 4, 3)  # is set on midnigth, the start of the day.
        
        start_date = current_date - pd.DateOffset(days=window_size)
        end_date = current_date
        print current_date, start_date, end_date
        # a query on the date range, for a specific pariticipant.
        
        data = []
        target = []
        datatime = []        
        for current_id in self.participants:
            mask = (self.df['id'] == current_id)

            # get every date for one person
            tf = self.df.loc[mask]
            tf = tf.ix[pd.to_datetime(tf.index).sort_values()]

            # get the time range that we are interested in
            time_range = tf[start_date:end_date]
            # print time_range

            # group by day
            a = np.unique(np.array(tf.index.map(pd.Timestamp.date)))
            count_days = 0
            groups = time_range.groupby(pd.TimeGrouper(freq='D'))
            for group in groups:
                window_data = []
                count_days += 1
                # g is a tuple, g[0] is the how the group is created, g[1] is the dataframe
                gdf = group[1]
                for var in self.variables:
                    varselection = gdf.loc[(gdf['variable'] == var)]
                    daymean = varselection['value'].mean()
                    print daymean
                    #daysum = varselection['value'].sum()
                    #dayvar = varselection['value'].var()  # variance
                    #print var, daymean, daysum, dayvar
                    if np.isnan(daymean):
                        pass
                    else:
                        # print current_id, start, end, var, five_day_mean, five_day_sum, five_day_var
                        window_data += [daymean]
                        
                    end = a[count_days]
                cur_day = tf[end:end + pd.DateOffset(days=1)]
                print cur_day
                mood_selection = cur_day.loc[(cur_day['variable'] == 'mood')]
                if len(mood_selection) > 0:
                    mood_mean = int(mood_selection['value'].mean())
                    print window_data
                    data.append(window_data)
                    datatime.append([a[count_days], current_id, window_data])
                    target.append(mood_mean)
        return np.array(data), np.array(target), self.participants, self.variables, datatime

    def window_combined_days(self, window_size):
        data = []
        target = []
        datatime = []
        for current_id in self.participants:
            mask = (self.df['id'] == current_id)

            # get every date for one person
            tf = self.df.loc[mask]
            tf = tf.ix[pd.to_datetime(tf.index).sort_values()]
            a = np.unique(np.array(tf.index.map(pd.Timestamp.date)))
            for i in range(len(a)):
                if i > window_size:
                    window_data = []
                    start = a[i - window_size]
                    end = a[i]
                    five_days_vars = tf[start:end]
                    for var in self.variables:
                        varselection = five_days_vars.loc[(five_days_vars['variable'] == var)]
                        five_day_mean = varselection['value'].mean()
                        five_day_mean = five_day_mean if not np.isnan(five_day_mean) else 0
                        five_day_sum = varselection['value'].sum()
                        five_day_sum = five_day_sum if not np.isnan(five_day_sum) else 0
                        five_day_var = varselection['value'].var()
                        five_day_var = five_day_var if not np.isnan(five_day_var) else 0
                        if np.isnan(five_day_mean):
                            pass
                            print current_id, start, end, var, five_day_mean, five_day_sum, five_day_var
                        else:
                            # print current_id, start, end, var, five_day_mean, five_day_sum, five_day_var
                            window_data += [five_day_mean, five_day_sum, five_day_var]
                    cur_day = tf[end:end + pd.DateOffset(days=1)]
                    mood_selection = cur_day.loc[(cur_day['variable'] == 'mood')]
                    if len(mood_selection) > 0:
                        mood_mean = int(mood_selection['value'].mean())
                        data.append(window_data)
                        datatime.append([a[i], current_id, window_data])
                        target.append(mood_mean)

                        # target.append()
        return np.array(data), np.array(target), self.participants, self.variables, datatime

import pandas as pd
from scipy.optimize import brute
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA
import numpy as np

class DataAggregator:
    def __init__(self, window_size=5):
        self.window_size = window_size

    def read(self, filepath):
        """
        Generates the aggregated data. For each day there is the average mood (the value) and the features.
        There are a few possible variables. For each variable we take the sum and the average over each day. These
        Will be the features.
        :param filepath:
        :return:
        """

        dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
        df = pd.read_csv(filepath, parse_dates=['time'], index_col='time', date_parser=dateparse)
        print df.keys()
        participants = df['id'].unique()  # all participants (don't know if needed)
        vars = df['variable'].unique()  # all possible variables

        current_date = pd.datetime(2014, 4, 3)  # is set on midnigth, the start of the day.
        start_date = current_date - pd.DateOffset(days=5)
        end_date = current_date
        print current_date, start_date, end_date
        # a query on the date range, for a specific pariticipant.
        current_id = 'AS14.01'
        mask = (df['id'] == current_id)
        
        # get every date for one person
        tf = df.loc[mask]
        tf = tf.ix[pd.to_datetime(tf.index).order()]
        #print tf
        #get the time range that we are interested in
        time_range = tf[start_date:end_date]
        #print time_range

        # group by day
        gs = time_range.groupby(pd.TimeGrouper(freq='D'))
        for g in gs:
            # g is a tuple, g[0] is the how the group is created, g[1] is the dataframe
            gdf = g[1]
            #print gdf
            for var in vars:
                varselection = gdf.loc[(gdf['variable'] == var)]
                daymean = varselection['value'].mean()
                daysum = varselection['value'].sum()
                dayvar = varselection['value'].var() #variance
                print var, daymean, daysum, dayvar
            break
        
        
        #print time_range.index
        #return
        a = np.unique(np.array(tf.index.map(pd.Timestamp.date)))
        for i in range(len(a)):
            if i > 5:
                start = a[i - 5]
                end = a[i]
                five_days_vars = tf[start:end]
                for var in vars:
                    #print var
                    varselection = five_days_vars.loc[(five_days_vars['variable'] == var)]
                    five_day_mean = varselection['value'].mean()
                    five_day_sum = varselection['value'].sum()
                    five_day_var = varselection['value'].var()
                    if np.isnan(five_day_mean):
                        print start, end, var, five_day_mean, five_day_sum, five_day_var
                    else:
                        print start, end, var, five_day_mean, five_day_sum, five_day_var
                    #print five_day_mean, five_day_sum, five_day_var
                    
                    
        #print ttf
        
        #df = df.set_index(['Timestamp'])     
        #print onedate
        # rolling window by 5 days
        #fivedaymean = time_range.resample('5D').mean()
        #maybe loop over the vars tomorrow morning
        #for var in vars:
        #    varselection = time_range.loc[(time_range['variable'] == var)]
        #    print varselection
            #a = varselection.rolling_window(time_range, window=5, win_type='parzen')
            #print a
        #fivedaysum = df.resample('D').sum().rolling(window=5).sum()
        #fivedayvar = df.resample('D').var().rolling(window=5).var()
        #print fivedaymean
        
    def objfunc(order, exog, endog):
        fit = ARIMA(endog, order, exog).fit()
        return fit.aic()


        grid = (slice(1, 3, 1), slice(1, 3, 1), slice(1, 3, 1))
        brute(objfunc, grid, args=(exog, endog), finish=None)      
        
        
  #Use ARIMAResults.predict to cross-validate alternative models. The best approach would be to keep the tail of the time series (say most recent 5% of data) out of sample, and use these points to obtain the test error of the fitted models.      
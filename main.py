import data_aggregator as dr

filepath = 'data/dataset_mood_smartphone.csv'
# filepath = 'data/dataset_small.csv'

data_aggregator = dr.DataAggregator()

# Reading the data
data_aggregator.read(filepath)


"""
http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.arima_model.ARIMA.html
Documentation on a arima implementation, should work with pandas stuff.


http://chrisstrelioff.ws/sandbox/2015/06/08/decision_trees_in_python_with_scikit_learn_and_pandas.html
a nice read about scikit, decision trees and pandas
"""

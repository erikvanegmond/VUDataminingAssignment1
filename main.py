import data_aggregator as dr
from scipy.optimize import brute
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import cross_validation

def test(window_size, data_aggregator):
    data, target = data_aggregator.read()
    print "\n\nTesting window size", window_size
    for _ in range(1):
        data_train, data_test, target_train, target_test = cross_validation.train_test_split(data, target, test_size=0.3)

        clf = DecisionTreeClassifier()
        clf = clf.fit(data_train, target_train)

        data_score = clf.score(data_test, target_test)
        print "score trained:", data_score

    data_score = clf.score(data_test, [3] * len(target_test))
    print "score 3:", data_score
    data_score = clf.score(data_test, [4] * len(target_test))
    print "score 4:", data_score
    data_score = clf.score(data_test, [5] * len(target_test))
    print "score 5:", data_score
    data_score = clf.score(data_test, [6] * len(target_test))
    print "score 6:", data_score
    data_score = clf.score(data_test, [7] * len(target_test))
    print "score 7:", data_score
    data_score = clf.score(data_test, [8] * len(target_test))
    print "score 8:", data_score


filepath = 'data/dataset_mood_smartphone.csv'
# filepath = 'data/dataset_small.csv'

data_aggregator = dr.DataAggregator(filepath)

for window_size in range(1, 6):
    test(window_size, data_aggregator)

# Reading the data



"""
http://statsmodels.sourceforge.net/devel/generated/statsmodels.tsa.arima_model.ARIMA.html
Documentation on a arima implementation, should work with pandas stuff.


http://chrisstrelioff.ws/sandbox/2015/06/08/decision_trees_in_python_with_scikit_learn_and_pandas.html
a nice read about scikit, decision trees and pandas
"""


def objfunc(order, exog, endog):
    fit = ARIMA(endog, order, exog).fit()
    return fit.aic()

    grid = (slice(1, 3, 1), slice(1, 3, 1), slice(1, 3, 1))
    brute(objfunc, grid, args=(exog, endog), finish=None)


    # Use ARIMAResults.predict to cross-validate alternative models. The best approach would be to keep the tail of the time series (say most recent 5% of data) out of sample, and use these points to obtain the test error of the fitted models.
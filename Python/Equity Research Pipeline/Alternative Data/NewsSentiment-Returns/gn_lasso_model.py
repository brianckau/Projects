import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.dates import *
from matplotlib.font_manager import *

import yfinance as yf

from sentiment_fetch import *
from gn_analytics import *

from sklearn.preprocessing import *
from sklearn.linear_model import *
from sklearn.pipeline import *
from sklearn.model_selection import *
from sklearn.metrics import make_scorer

def regression_model_returns_prediction(sentiment_analysis_df,n_splits=2, x_days_later=1):


    if x_days_later == 0:
        X = sentiment_analysis_df.iloc[:,1:]
        Y = sentiment_analysis_df.iloc[:,0]

    elif x_days_later >= 0:
        X = sentiment_analysis_df.iloc[:,1:].iloc[:-x_days_later]
        Y = sentiment_analysis_df.iloc[:,0].shift(-x_days_later).iloc[:-x_days_later]


    pipeline = Pipeline([('scaler', StandardScaler()),
                        ('lasso', Lasso())])
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    param_grid = {'lasso__alpha': [0.001,0.01,0.1,1.0,10,100]}

    IC = make_scorer(information_coefficient,greater_is_better=True)

    optimal_model = GridSearchCV(estimator=pipeline,
                                param_grid=param_grid,
                                cv=tscv,
                                scoring = IC,
                                verbose=1)
    
    optimal_model.fit(X,Y)

    print('------------------------------------------------------')
    print(f'The IC of the model is: {round(optimal_model.best_score_,5)}')

    if np.abs(optimal_model.best_score_) >= 0.08:
        print(f'the model is extremely useful')
    elif np.abs(optimal_model.best_score_) > 0.05:
        print(f'the model is highly useful')
    elif np.abs(optimal_model.best_score_) > 0.02:
        print(f'the model is good')
    elif np.abs(optimal_model.best_score_) > 0:
        print(f'the model is weak')
    else:
        print(f'the model captures only random noise')

    return optimal_model


def information_coefficient(y_true, y_pred):
    if np.std(y_pred) == 0:
        return 0.0
    else:
        return np.corrcoef(y_true, y_pred)[0,1]
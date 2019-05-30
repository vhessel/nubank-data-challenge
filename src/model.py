from sklearn.base import BaseEstimator, ClassifierMixin
from lightgbm import LGBMClassifier, LGBMRegressor, LGBMModel
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

class NullModelClassifier(BaseEstimator, ClassifierMixin):
    """"" 
    Dummy Null-Model Classifier. There is no practical utility besides test the model pipeline
    """
    def __init__(self):
        pass
    def fit(self, X, y, **fit_params):
        print("Fit X: ")
        print(X)
        return self
    def predict(self, X):
        """ 
        We found the unconditional default rate is 16.0% in the notebook 02_credit_risk_eda.ipynb
        """
        print("Predict X")
        print(X)
        return pd.DataFrame(0.16*np.ones((X.shape[0],1)), columns=['PredictedClass'])
        
class LGBMClassifierWrapper(LGBMClassifier):
    def fit(self, X, y, **fit_params):
        if np.unique(np.round(y)).shape[0]==2:
            stratification = y
        else:
            stratification = None
        train_idx, valid_idx = train_test_split(np.arange(X.shape[0]), test_size=0.2, stratify=stratification )
        X_train = X[train_idx]
        y_train = y[train_idx]
        X_val= X[valid_idx]
        y_val= y[valid_idx]        
        eval_set=[(X_val,y_val),]
        return super(LGBMClassifierWrapper, self).fit(X_train, y_train, eval_set=eval_set, **fit_params)
        
class LGBMRegressorWrapper(LGBMModel):
    def fit(self, X, y, **fit_params):
        train_idx, valid_idx = train_test_split(np.arange(X.shape[0]), test_size=0.2)
        X_train = X[train_idx]
        y_train = y[train_idx]
        X_val= X[valid_idx]
        y_val= y[valid_idx]        
        eval_set=[(X_val,y_val),]
        return super(LGBMRegressorWrapper, self).fit(X_train, y_train, eval_set=eval_set, **fit_params)
        

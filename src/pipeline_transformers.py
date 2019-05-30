from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.decomposition import PCA
import numpy as np
import numpy
import pandas as pd
import scipy.stats as st


""" 
This module aims to provide transformers to the Input Pipeline that receive the raw data
and return a suitable data set to be used in the models.
"""

class NullPreprocessingPipeline(BaseEstimator, TransformerMixin):
    """ 
    Dummy preprocessing pipeline for the Null-Model. There is no practical utility besides test the model pipeline
    """
    def __init__(self):
        pass
    def fit(self, X, y=None, **fit_params):
        return self
    def transform(self, X, y=None):
        return pd.DataFrame(np.zeros((X.shape[0],1)),columns=['NullFeature'])

class IdentityTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y = None, **fit_params):
        return self
    def transform(self, X, y = None):
        return X
    
class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        try:
            return X[self.columns]
        except KeyError:
            cols_error = [x for x in set(self.columns) - set(X.columns)]
            raise KeyError("Columns not found: %s" % cols_error)
    
class TypeSelector(BaseEstimator, TransformerMixin):
    def __init__(self, include_dtypes=None, exclude_dtypes=None):
        self.include_dtypes = include_dtypes
        self.exclude_dtypes = exclude_dtypes
    def fit(self, X, y=None, **fit_params):
        return self
    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        if self.include_dtypes is not None:
            result = X.select_dtypes(include = self.include_dtypes)
            if result.shape[1] == 0:
                result = pd.DataFrame(np.zeros((X.shape[0],1)), columns=['null_column'])
            return result
        elif self.exclude_dtypes is not None:
            return X.select_dtypes(exclude = self.exclude_dtypes)
        else:
            raise ValueError('include_dtypes and exclude_dtypes should not be simultaneously None')

class CategoryConstrainer(BaseEstimator, TransformerMixin):
    def __init__(self, min_occurrences=1):
        self.min_occurrences = min_occurrences
    def fit(self, X, y=None, **fit_params):
        assert isinstance(X, pd.DataFrame)
        self._col_dict = {}
        for c in X.columns:
            map_int = {k:(i if pd.isnull(k)==False else np.nan) for i,k in enumerate(X[c].unique())}
            occurences = X[c].value_counts()
            occurences = occurences[occurences>0].to_dict()
            for k,v in occurences.items():
                if v < self.min_occurrences:
                    map_int.pop(k)
            self._col_dict[c]=map_int
        return self
    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X = X.copy()
        for c in X.columns:
            X[c] = X[c].map(self._col_dict.get(c))
        return X

class CustomOrdinalEncoder(TransformerMixin):
    def __init__(self, min_occurrences = 1):
        """ Transform categorical features into integer values. If a category apears less times than
        min_occurences, it is replaced to NaN. min_occurences can be used to reduce the overfitting. 
        
        Parameters
        ----------
        min_occurrences: int, optional
            Minimum number of occurences a value must have to be encoded as a number, otherwise it will be replaced tiwh NaN
        """
        self._min_occurences = min_occurrences
    
    def fit(self, X, y=None, **fit_params):
        assert isinstance(X,np.ndarray)
        self._maps = {}
        for c in range(X.shape[1]):
            map_int = {k:(i if (k is not None and pd.isnull(k)==False) else np.nan) for i,k in enumerate(np.unique(X[:,c]))}
            occurences = pd.Series(X[:,c]).value_counts().to_dict()
            for k,v in occurences.items():
                print(v)
                if v < self._min_occurences:
                    map_int.pop(k)
            self._maps[c] = map_int
        return self
            
    def transform(self, X, y=None):
        assert isinstance(X,np.ndarray)
        result = X.copy()
    
        for c in range(X.shape[1]):
            assert (self._maps.get(c) is not None)
            result[:,c] = pd.Series(result[:,c]).map(self._maps.get(c)).values
            
        return result
            
class NumericEncoder(TransformerMixin):
    def __init__(self, min_occurrences = 1):
        """ Transform categorical features into integer values. If a category apears less times than
        min_occurences, it is replaced to NaN. min_occurences can be used to reduce the overfitting. 
        
        Parameters
        ----------
        min_occurrences: int, optional
            Minimum number of occurences a value must have to be encoded as a number, otherwise it will be replaced tiwh NaN
        """
        self._min_occurences = min_occurrences
    
    def fit(self, X, y=None, **fit_params):
        self._maps = {}
        self._feature_names = X.columns
        for c in X.columns:
            map_int = {k:(i if (k is not None and pd.isnull(k)==False) else np.nan) for i,k in enumerate(X[c].unique())}
            occurences = X[c].value_counts().to_dict()
            for k,v in occurences.items():
                if v < self._min_occurences:
                    map_int.pop(k)
            self._maps[c] = map_int
        return self
            
    def transform(self, X, y=None):
        result_df = X.copy()
    
        for c in X.columns:
            assert (self._maps.get(c) is not None)
            result_df[c] = result_df[c].map(self._maps.get(c))
            
        return result_df
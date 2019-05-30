from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import ast

""" 
This module aims to provide Feature Engineering modules that receive the raw data
and return a set of created features.
"""

class GeneralFeatureEngineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y = None, **fit_params):
        assert isinstance(X, pd.DataFrame)
        X = X.copy()
        
        self._data_mean = X.select_dtypes(exclude=['category']).mean()
        self._data_std = X.select_dtypes(exclude=['category']).std()
        
        X['score_3_squared'] = (X['score_3']-self._data_mean['score_3'])**2
        X['score_4_squared'] = (X['score_4']-self._data_mean['score_4'])**2
        X['score_5_squared'] = (X['score_5']-self._data_mean['score_5'])**2
        X['score_6_squared'] = (X['score_6']-self._data_mean['score_6'])**2
        X['score_3_times_score_6'] = X['score_3']*X['score_6']
        X['score_4_times_score_6'] = X['score_4']*X['score_6']
        X['score_5_times_score_6'] = X['score_5']*X['score_6']
        X['score_3_sum2_score_4'] = (X['score_3']-self._data_mean['score_3'])**2+(X['score_4']-self._data_mean['score_4'])**2
        X['score_3_sum2_score_6'] = (X['score_3']-self._data_mean['score_3'])**2+(X['score_6']-self._data_mean['score_6'])**2
        X['score_4_sum2_score_6'] = (X['score_4']-self._data_mean['score_4'])**2+(X['score_6']-self._data_mean['score_6'])**2
        self._pca_cols = ['score_3','score_4','score_5','score_6',
                    'score_3_squared', 'score_4_squared', 'score_5_squared', 'score_6_squared',
                    'score_3_sum2_score_4', 'score_3_sum2_score_6', 'score_4_sum2_score_6',
                    'score_3_times_score_6', 'score_4_times_score_6', 'score_5_times_score_6',]
        X[self._pca_cols] = X[self._pca_cols].fillna(0)
        self._score_pca = PCA(n_components=5).fit((X[self._pca_cols]-X[self._pca_cols].mean())/X[self._pca_cols].std())
        
        
        # Profile Tags
        tags_train = X['profile_tags'].astype(str).apply(ast.literal_eval).apply(lambda x: x.get('tags'))
        self._tags = np.unique([x[0] for x in tags_train])
        
        return self
    
    def transform(self, X, y = None):
        assert isinstance(X, pd.DataFrame)
        X = X.copy()
        
        X['score_3_squared'] = (X['score_3']-self._data_mean['score_3'])**2
        X['score_4_squared'] = (X['score_4']-self._data_mean['score_4'])**2
        X['score_5_squared'] = (X['score_5']-self._data_mean['score_5'])**2
        X['score_6_squared'] = (X['score_6']-self._data_mean['score_6'])**2
        X['income_square'] = (X['income']-self._data_mean['income'])**2
        X['reported_income_square'] = X['reported_income']**2
        X['log_income_square'] = (X['log_income']-self._data_mean['log_income'])**2
        X['log_reported_income_square'] = X['log_reported_income']**2
        
        X['score_3_times_score_6'] = X['score_3']*X['score_6']
        X['score_4_times_score_6'] = X['score_4']*X['score_6']
        X['score_5_times_score_6'] = X['score_5']*X['score_6']
        X['reported_income_times_income'] = (X['reported_income']*X['income']/1e10)
        
        X['score_3_sum2_score_4'] = (X['score_3']-self._data_mean['score_3'])**2+(X['score_4']-self._data_mean['score_4'])**2
        X['score_3_sum2_score_6'] = (X['score_3']-self._data_mean['score_3'])**2+(X['score_6']-self._data_mean['score_6'])**2
        X['score_4_sum2_score_6'] = (X['score_4']-self._data_mean['score_4'])**2+(X['score_6']-self._data_mean['score_6'])**2
        X['reported_income_sum2_income'] = (X['reported_income']-self._data_mean['reported_income'])**2+(X['income']-self._data_mean['income'])**2
        
        X['credit_limit_per_income'] = X['credit_limit']/X['income']
        X['credit_limit_per_borrow'] = X['credit_limit']/X['last_amount_borrowed']
        X['reported_income_per_income'] = X['reported_income']/X['income']
        X['borrow_per_income'] = X['last_amount_borrowed']/X['income']
        X['reported_income_per_credit_limit'] = (X['reported_income']/X['credit_limit']).replace([-np.inf, np.inf],np.nan)
        
        X['credit_limit_minus_reported_income'] = X['reported_income']-X['credit_limit']
        X['reported_income_minus_income'] = X['reported_income']-X['income']
        
        
        X['facebook_profile_state'] = (X['facebook_profile'].astype(str)+X['state'].astype(str)).astype('category')
        X['state_shipping_state'] = (X['state'].astype(str)+X['shipping_state'].astype(str)).astype('category')
        
        X['log_income_reported_income_square'] = (X['log_income']-self._data_mean['log_income'])**2+(X['log_reported_income']-self._data_mean['log_reported_income'])**2
        
        X['estimated_state_shipping_state'] = (X['estimated_state'].astype(str)==X['shipping_state'].astype(str)).astype('category')
        
        X['last_amount_borrowed_income_interaction'] = (X['income']-self._data_mean['income'])/self._data_std['income'] + (X['last_amount_borrowed']-self._data_mean['last_amount_borrowed'])/self._data_std['last_amount_borrowed']
        
        X['low_reported_income'] = (X['income']<50000).astype("category")
        
        data_pca = X[self._pca_cols].copy().fillna(0)
        data_pca = ((data_pca-data_pca.mean())/data_pca.std()).replace([-np.inf,np.inf],0)
        data_pca = pd.DataFrame(self._score_pca.transform(data_pca), columns=['score_pca_1','score_pca_2','score_pca_3','score_pca_4','score_pca_5'], index=X.index)
        X = X.join(data_pca, how='left')
        
        tags_data = X['profile_tags'].astype(str).apply(ast.literal_eval).apply(lambda x: x.get('tags'))
        for t in self._tags:
            X[t] = tags_data.apply(lambda x: t in x).astype(np.uint8)
        
        return X

class ZScoreFeatureEngineering(BaseEstimator, TransformerMixin):
    """
    This class creates new features based on aggregation of columns in a set of
    other features. It provide a Z-Score using the mean and standard deviation
    from the groups aggregated
    """
    def __init__(self):
        pass
    def fit(self, X, y = None, **fit_params):
        assert isinstance(X, pd.DataFrame)
        self._zscore = [
                (['state'],'income',np.mean,'state_income_mean'),
                (['state'],'income',np.std,'state_income_std'),
                (['state'],'score_3',np.mean,'state_score_3_mean'),
                (['state'],'score_3',np.std,'state_score_3_std'),
                (['state'],'score_4',np.mean,'state_score_4_mean'),
                (['state'],'score_4',np.std,'state_score_4_std'),
                (['state'],'score_5',np.mean,'state_score_5_mean'),
                (['state'],'score_5',np.std,'state_score_5_std'),
                (['state'],'score_6',np.mean,'state_score_6_mean'),
                (['state'],'score_6',np.std,'state_score_6_std'),
                (['state'],'risk_rate',np.mean,'state_risk_rate_mean'),
                (['state'],'risk_rate',np.std,'state_risk_rate_std'),
                (['state'],'credit_limit',np.mean,'state_credit_limit_mean'),
                (['state'],'credit_limit',np.std,'state_credit_limit_std'),
                (['state'],'application_time_applied',np.mean,'state_application_time_applied_mean'),
                (['state'],'application_time_applied',np.std,'state_application_time_applied_std'),
                (['state'],'lat',np.mean,'state_lat_mean'),
                (['state'],'lat',np.std,'state_lat_std'),
                (['state'],'lon',np.mean,'state_lon_mean'),
                (['state'],'lon',np.std,'state_lon_std'),
                (['state'],'last_amount_borrowed',np.mean,'state_last_amount_borrowed_mean'),
                (['state'],'last_amount_borrowed',np.std,'state_last_amount_borrowed_std'),
                (['state'],'external_data_provider_email_seen_before',np.mean,'state_external_data_provider_email_seen_before_mean'),
                (['state'],'external_data_provider_email_seen_before',np.std,'state_external_data_provider_email_seen_before_std'),
                (['state'],'external_data_provider_fraud_score',np.mean,'state_external_data_provider_fraud_score_mean'),
                (['state'],'external_data_provider_fraud_score',np.std,'state_external_data_provider_fraud_score_std'),
                (['real_state','state'], 'income', np.mean, 'real_state_state_income_mean'),
                (['real_state','state'], 'income', np.std, 'real_state_state_income_std'),
                (['email'], 'external_data_provider_email_seen_before', np.mean, 'email_external_data_provider_email_seen_before_mean'),
                (['email'], 'external_data_provider_email_seen_before', np.std, 'email_external_data_provider_email_seen_before_std'),
                (['facebook_profile'], 'income', np.mean, 'facebook_profile_income_mean'),
                (['facebook_profile'], 'income', np.std, 'facebook_profile_income_std'),
                (['user_agent'], 'income', np.mean, 'user_agent_income_mean'),
                (['user_agent'], 'income', np.std, 'user_agent_income_std'),
                (['estimated_district'],'income',np.mean,'estimated_district_income_mean'),
                (['estimated_district'],'income',np.std,'estimated_district_income_std'),
               ]
        self._data_zscore = []
        for agg in self._zscore:
                self._data_zscore.append((agg[0],agg[1], X.groupby(agg[0])[agg[1]].apply(agg[2]).to_frame(name=agg[3]).reset_index()))
        

        return self

    def transform(self, X, y = None):
        assert isinstance(X, pd.DataFrame)
        X = X.copy() 
        reconstructed_data = pd.DataFrame([], index=X.index)
        for agg,_,d in self._data_zscore:
            merged = X[agg].merge(d, how='left', on=agg)
            reconstructed_data[merged.columns[-1]] = merged.iloc[:,-1].values

        #AGGREGATION-BASED FEATURES
        for agg,feat,_,_ in self._zscore:
            agg_name = '_'.join(agg)
            col_name = agg_name + '_' + feat
            X['zscore_' + col_name] = ((X[feat]-reconstructed_data[col_name + '_mean'])/reconstructed_data[col_name + '_std']).replace([-np.inf, np.inf], np.nan).astype(X[feat].dtype)
            X[col_name + '_mean'] = reconstructed_data[col_name + '_mean']
        
        #Features Bases on the mean of aggregations
        X['distance_state'] = np.abs(X['lat']-reconstructed_data['state_lat_mean'])+(X['lon']-reconstructed_data['state_lon_mean'])
        X['distance_state_lat'] = X['lat']-reconstructed_data['state_lat_mean']
        X['distance_state_lon'] = X['lon']-reconstructed_data['state_lon_mean']

        return X

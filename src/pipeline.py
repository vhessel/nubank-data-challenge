from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, cross_val_predict, cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, accuracy_score, roc_auc_score, fbeta_score, r2_score, mean_squared_error, explained_variance_score, f1_score
from sklearn.pipeline import Pipeline, make_pipeline, FeatureUnion
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, RidgeClassifier, SGDClassifier
from sklearn.linear_model import Lasso, ElasticNet, LassoLars, LinearRegression
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import VarianceThreshold
import lightgbm as lgbm
import numpy as np
import pandas as pd
import json
from glob import glob
import os
import gc
import pickle

from .pipeline_util import set_up_model, set_up_experiment
import src.data_util as du
from src.feature_engineering import *
from src.pipeline_transformers import *
from src.model import *
from src.functions import *

class GenericPipeline(object):
    """ 
    Class that implements a generic pipeline to be used in the problems
    """

    def __init__(self, action, EXP_CONF):
        self._EXP_CONF = EXP_CONF
        set_up_experiment(EXP_CONF)
        self.execute_action(action)


    def execute_action(self, a):
        if a == 'train' or a == 'grid_search' or a == 'cross_validation' or a == 'save_oof':
            self.training(a)
        elif a == 'final_validation':
            self.evaluate(a)    
        elif a == 'predict':
            self.predict(a)
        else:
            raise NotImplementedError('CreditRiskModel: Action Not Implemented - ' + a)
        
    def predict(self, action):
        """
        Prediction procedure
        """
        prediction_path = self._EXP_CONF.get('prediction_path')
        data_path = self._EXP_CONF.get('data_path')
        files = glob(os.path.join(prediction_path,'*.csv'))
        main_pipeline = self.deserialize_pipeline()
        post_processing = self._EXP_CONF.get('prediction_post_processing','identity_function')
        post_processing = globals()[post_processing ]
        
        for f in files:
            new_data = du.load_acquisition_file(f, data_path )
            y_pred = main_pipeline.predict(new_data)
            y_pred = post_processing(new_data, y=y_pred)
            if isinstance(y_pred,pd.DataFrame) or isinstance(y_pred,pd.Series):
                pred_df = pd.DataFrame(y_pred.values, columns=['predictions'], index=new_data['ids'])
            else:
                pred_df = pd.DataFrame(y_pred, columns=['predictions'], index=new_data['ids'])
            pred_df.fillna('NaN').to_csv(os.path.join(prediction_path, 'predictions',self._EXP_CONF.get('model_name') + '_' + os.path.basename(f)))
            
            
        
        
    def evaluate(self, action):
        """
        Evaluation procedure
        """
        X_test, y_test = self.load_training_data(final_validation = True)
        
        #Load serialized pipeline
        main_pipeline = self.deserialize_pipeline()
        self.build_metrics()
        self.write_final_validation_results(main_pipeline, X_test, y_test)
            
        
    def training(self, action = None):
        """ 
        Training procedure            
        """        
        X_train, y_train = self.load_training_data()
        
        self.kfold_gen, y = self.get_kfold_generator(X_train, y_train)
        
        # ------------ Pipeline Configuration --------------
        self.build_preprocessing_pipeline()
        self.build_model_estimator()
        self.build_metrics()
        
        main_pipeline = Pipeline([('preprocessing', self._preprocessing_pipeline),
                                 ('model', self._model)])
        main_pipeline.set_params(**self._EXP_CONF.get('model_params',{}))
        
        # ------------ Implemented Actions ----------------
        if action == 'grid_search':
            grid_search = GridSearchCV(main_pipeline, self._EXP_CONF.get('grid_search_params'), scoring=self._metrics, 
                                       cv = self.kfold_gen, n_jobs = -1, verbose=2, refit='fbeta')
            grid_search.fit(X_train, y_train)
            print(grid_search.best_score_)
            print(grid_search.best_params_)
            if self._EXP_CONF.get('grid_search_save_best_pipeline', False):
                self.serialize_pipeline(grid_search.best_estimator_)
        elif action == 'cross_validation':
            cv_results = cross_validate(main_pipeline, X_train, y_train, cv=self.kfold_gen, 
                                        fit_params=self._EXP_CONF.get('fit_params'),
                                        return_estimator=True, scoring=self._metrics, n_jobs=1)
            self.write_cv_results(cv_results, X_train, y_train)
        elif action == 'train':
            main_pipeline.fit(X_train, y_train)
            self.serialize_pipeline(main_pipeline)
        else:
            raise NotImplementedError('CreditRiskModel: Training Action Not Implemented - ' + action)

    def write_final_validation_results(self, main_pipeline, X_test, y_test):
        
        validation_path = os.path.join(self._EXP_CONF.get('experiment_path'), 'final_validation')
        metrics = {}
        for k,m in self._metrics.items():
            metrics[k] = m(main_pipeline, X_test, y_true = y_test)
        results_df = pd.DataFrame(metrics, index=['validation_results'])
        results_df.to_csv(os.path.join(validation_path,'results.csv'), index=False)
        
        with open(os.path.join(validation_path , 'experiment_conf.txt'),'w') as file:
            json.dump(self._EXP_CONF,file)
        
        
        y_pred = main_pipeline.predict(X_test)
        oof_df = pd.Series(y_test.copy()).to_frame('y_true')
        oof_df['y_oof'] = y_pred
        oof_df.to_csv(os.path.join(validation_path,'oof_predictions.csv'), index=False)
        
        feature_names = self._EXP_CONF.get('x_features')
        feature_importances = []
        e = main_pipeline.steps[-1][1]
        if hasattr(e,'feature_importances_'):
            feature_importances = e.feature_importances_
        try:
            if len(feature_importances)==0:
                feature_importances = np.zeros_like(feature_names)
            
            feature_importances_df = pd.DataFrame(feature_importances, columns=['feat_importance'])
            if len(feature_names) == feature_importances_df.shape[0]:
                feature_importances_df['feat_name'] =  feature_names
            else:
                feature_importances_df['feat_name'] =  ['feat_%d'%i for i in range(feature_importances_df.shape[0])]
        except:
            feature_importances_df = pd.DataFrame([], columns=['feat_name','feat_importance'])
        feature_importances_df.to_csv(os.path.join(validation_path,'feature_importances.csv'), index=False)

    def write_cv_results(self, cv_results, X_train, y_train):
        results_path = os.path.join(self._EXP_CONF.get('experiment_path'), 'cv_results')
        
        results_df = pd.DataFrame.from_dict(cv_results)
        results_df.drop('estimator', axis=1, inplace=True)
        results_df.loc['std',:] = results_df.std().values
        results_df.loc['mean',:] = results_df.iloc[:-1,:].mean().values
        results_df = results_df.reset_index().rename(columns={'index':'fold'})
        results_df.to_csv(os.path.join(results_path,'results.csv'), index=False)

        X_train.to_csv(os.path.join(results_path, 'X_train.csv'), index=False)
        
        with open(os.path.join(results_path, 'experiment_conf.txt'),'w') as file:
            json.dump(self._EXP_CONF,file)
            
        # Get out-of-fold predictions
        y_oof = pd.Series(y_train.copy())
        for i, (_, val_idx) in enumerate(self.kfold_gen.split(np.arange(X_train.shape[0]), y=y_train)):
            y_oof.iloc[val_idx] = cv_results['estimator'][i].predict(X_train.iloc[val_idx,:])
        
        post_processing = self._EXP_CONF.get('prediction_post_processing', 'identity_function')
        post_processing = globals()[post_processing]
        oof_df = y_oof.to_frame(name='y_oof')
        oof_df['y_true'] = y_train
        oof_df['y_true'] = post_processing(X_train, y_train)
        oof_df['y_oof'] = post_processing(X_train, y_oof.values)
        oof_df.to_csv(os.path.join(results_path,'oof_predictions.csv'), index=False)
        
        feature_names = self._EXP_CONF.get('x_features')
        feature_importances = []
        
        for p in cv_results['estimator']:
            e = p.steps[-1][1]
            if hasattr(e,'feature_importances_'):
                feature_importances.append(np.atleast_2d(e.feature_importances_).T)
            elif hasattr(e,'coef_'):
                feature_importances.append(np.atleast_2d(e.coef_).T)
        
        try:
            if len(feature_importances)==0:
                feature_importances = np.zeros_like(feature_names)
            else:
                feature_importances = np.mean(np.abs(np.concatenate(feature_importances,axis=-1)),axis=-1)
            
            feature_importances_df = pd.DataFrame(feature_importances, columns=['feat_importance'])
            if len(feature_names) == feature_importances_df.shape[0]:
                feature_importances_df['feat_name'] =  feature_names
            else:
                feature_importances_df['feat_name'] =  ['feat_%d'%i for i in range(feature_importances_df.shape[0])]
        except:
            feature_importances_df = pd.DataFrame([], columns=['feat_name','feat_importance'])
        feature_importances_df.to_csv(os.path.join(results_path,'feature_importances.csv'), index=False)

    def serialize_pipeline(self, pipeline):
        with open(os.path.join(self._EXP_CONF.get('experiment_path'), 'checkpoint', 'pipeline.pkl'), 'wb') as file:
                pickle.dump(pipeline, file)
    def deserialize_pipeline(self):
        with open(os.path.join(self._EXP_CONF.get('experiment_path'), 'checkpoint', 'pipeline.pkl'), 'rb') as file:
            pipeline = pickle.load(file)
        return pipeline
        
    def get_kfold_generator(self, X=None, y=None):
        """ 
        Method to create a KFold Generator
        Its a place to implement the stratification strategies, for example
        """
        kfold_strategy = self._EXP_CONF.get('kfold_strategy','random')
        if  kfold_strategy == 'random':
            kfold = KFold(n_splits= self._EXP_CONF.get('n_folds',5), shuffle=True, random_state=self._EXP_CONF.get('random_seed'))
            y = None
        elif kfold_strategy == 'stratified':
            kfold = StratifiedKFold(n_splits = self._EXP_CONF.get('n_folds',5), shuffle=True, random_state=self._EXP_CONF.get('random_seed'))                
        else:
            raise NotImplementedError('CreditRiskModel: KFold Strategy Not Implemented - ' + kfold_strategy)
            
        return kfold, y
        
    def build_preprocessing_pipeline(self):
        """ 
        Configure the preprocessing pipeline 
        For now, its just build an object of a pipeline implemented externally
        """
        cat_transformer = globals()[self._EXP_CONF.get('cat_transformer','OrdinalEncoder')]
        cat_transformer = cat_transformer()
        pipeline_categorical = Pipeline([
                ('col_selector', TypeSelector(include_dtypes=['category'])),
                ('constrainer', CategoryConstrainer()),
                ('missing_strat', SimpleImputer(strategy = 'constant')),
                ('transformer', cat_transformer)
                                     ])
    
        num_transformer = globals()[self._EXP_CONF.get('num_transformer','IdentityTransformer')]
        num_transformer = num_transformer()
        pipeline_numerical = Pipeline([
                ('col_selector', TypeSelector(exclude_dtypes=['category'])),
                ('missing_strat', SimpleImputer(strategy = 'constant')),
                ('transformer', num_transformer)
                ])

        feat_steps = [(x[0], globals()[x[1]]()) for x in self._EXP_CONF.get('feat_engineering')]
        feat_eng = Pipeline(feat_steps)
        self._preprocessing_pipeline = Pipeline([
                ('feat_engineering', feat_eng),
                ('col_selector', ColumnSelector(self._EXP_CONF.get('x_features'))),
                ('feat_union', FeatureUnion([
                        ('cat_features', pipeline_categorical),
                        ('num_features', pipeline_numerical)
                        ])),
                ('var_threshold', VarianceThreshold()),
                ])
        self._preprocessing_pipeline.set_params(**self._EXP_CONF.get('pipeline_parameters'))
    
        
    def build_model_estimator(self):
        """
        Configure the model (classifier)
        """
        model = globals()[self._EXP_CONF.get('model')]
        self._model = model()
        #self._model.set_params(**self._EXP_CONF.get('model_params',{}))
        
    
    def build_metrics(self):
        """
        Define the metrics used to evaluate the model
        """
        self._metrics = {name:make_scorer(globals()[x.get('score')], **x.get('params',{})) for name,x in self._EXP_CONF.get('model_metrics').items()}
        
        
    def load_training_data(self, final_validation = False):
        """
        Load the data to training and validation
        """
        data, _ = du.load_data_preprocessed(self._EXP_CONF.get('data_path'))
        
        #Remove rows with target missing
        data = data.loc[data[self._EXP_CONF.get('y_target')].notnull(),:]
        
        X_data = data.drop(self._EXP_CONF.get('y_target'), axis=1)
        y_data = data[self._EXP_CONF.get('y_target')].values
        if y_data.dtype==np.object:
            y_data = y_data.astype(np.uint8)
        del data
        gc.collect()
        
        train_idx, test_idx= train_test_split(np.arange(X_data.shape[0]), test_size = self._EXP_CONF.get('test_size'), random_state = self._EXP_CONF.get('random_seed'))
        if not final_validation:
            X = X_data.iloc[train_idx,:]
            y = y_data[train_idx]
        else:
            X = X_data.iloc[test_idx,:]
            y = y_data[test_idx]
        return X, y
            
        
        

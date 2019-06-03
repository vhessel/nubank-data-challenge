import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin
import ast
import os
import reverse_geocoder as rg

TARGET_VARS = ['target_default', 'target_fraud']

QUANTITATIVE_RAW_VARS = ['score_3', 'score_4', 'score_5', 'score_6', 'risk_rate','last_amount_borrowed', 'last_borrowed_in_months', 
              'credit_limit','income', 'ok_since', 'n_bankruptcies', 'n_defaulted_loans','n_accounts', 'n_issues', 
              'application_time_in_funnel', 'external_data_provider_credit_checks_last_2_year',
              'external_data_provider_credit_checks_last_month','external_data_provider_credit_checks_last_year',
              'external_data_provider_email_seen_before', 'external_data_provider_fraud_score', 'reported_income','application_time_applied',
              'lat_lon']

QUALITATIVE_RAW_VARS = ['ids', 'score_1', 'score_2', 'reason', 'facebook_profile', 'state', 'zip', 'channel', 
             'job_name', 'real_state', 'email', 'external_data_provider_first_name', 'marketing_channel', 
             'profile_phone_number', 'shipping_state', 'profile_tags', 'user_agent','shipping_zip_code']



QUALITATIVE_VARS = ['ids', 'score_1', 'score_2', 'reason', 'facebook_profile', 'state', 'zip', 'channel', 
             'job_name', 'real_state', 'email', 'external_data_provider_first_name', 'marketing_channel', 
             'profile_phone_number', 'shipping_state', 'profile_tags', 'user_agent','shipping_zip_code',
             'estimated_state','estimated_district', 'estimated_gender']

QUANTITATIVE_VARS = ['score_3', 'score_4', 'score_5', 'score_6', 'risk_rate','last_amount_borrowed', 'last_borrowed_in_months', 
              'credit_limit','income', 'ok_since', 'n_bankruptcies', 'n_defaulted_loans','n_accounts', 'n_issues', 
              'application_time_in_funnel', 'external_data_provider_credit_checks_last_2_year',
              'external_data_provider_credit_checks_last_month','external_data_provider_credit_checks_last_year',
              'external_data_provider_email_seen_before', 'external_data_provider_fraud_score', 'reported_income','application_time_applied',
              'lat','lon']

estimated_states_map = {'Acre':'BR-AC','Alagoas':'BR-AL','Amapa':'BR-AP','Amazonas':'BR-AM','Bahia':'BR-BA','Ceara':'BR-CE','Distrito Federal':'BR-DF','Espirito Santo':'BR-ES','Goias':'BR-GO',
'Maranhao':'BR-MA','Mato Grosso':'BR-MT','Mato Grosso do Sul':'BR-MS','Minas Gerais':'BR-MG','Para':'BR-PA','Paraiba':'BR-PB','Parana':'BR-PR','Pernambuco':'BR-PE',
'Piaui':'BR-PI','Rio de Janeiro':'BR-RJ','Rio Grande do Norte':'BR-RN','Rio Grande do Sul':'BR-RS','Rondonia':'BR-RO','Roraima':'BR-RR','Santa Catarina':'BR-SC',
'Sao Paulo':'BR-SP','Sergipe':'BR-SE','Tocantins':'BR-TO'}

def load_data(data_path):
    """ 
    Load the CSV files  
    """
    acquisition_train = pd.read_csv(os.path.join(data_path,'data/acquisition_train.csv.gz'))
    acquisition_test = pd.read_csv(os.path.join(data_path, 'data/acquisition_test.csv.gz'))
    spend_train = pd.read_csv(os.path.join(data_path, 'data/spend_train.csv.gz'))

    return acquisition_train, spend_train, acquisition_test


def load_data_preprocessed(data_path):
    """ 
    Load the data for the training phase
    """
    #acquisition_train = pd.read_csv(os.path.join(data_path,'data/acquisition_train.csv'), dtype=dtypes)
    spend_train = pd.read_csv(os.path.join(data_path, 'data/spend_train.csv.gz'))
    acquisition_train, spend_train = load_acquisition_file(os.path.join(data_path,'data/acquisition_train.csv.gz'),data_path , targets_spend_file=spend_train)
    #acquisition_test = pd.read_csv(os.path.join(data_path, 'data/acquisition_test.csv'), dtype=dtypes)
    return acquisition_train, spend_train    

    
def load_acquisition_file(filename, data_path, targets_spend_file = None):
    """ 
    Load the CSV files and applies pre-processing transformations set from
    analysis of notebook 01_initial_eda.ipynb
    """
    dtypes = {'ids':str, 'score_1':str, 'score_2':str, 'reason':str, 'facebook_profile':str, 'state':str, 'zip':str,
              'channel':str, 'job_name':str, 'real_state':str, 'email':str, 'external_data_provider_first_name':str,
              'marketing_channel':str, 'profile_phone_number':str, 'shipping_state':str, 'profile_tags':str,
              'user_agent':str,'shipping_zip_code':str, 'external_data_provider_fraud_score': np.float32}

    
    acquisition = pd.read_csv(filename, dtype=dtypes)
    
    # Reported Income
    acquisition.loc[acquisition['reported_income']>acquisition['income'].mean()+3*acquisition['income'].std(),'reported_income'] = np.nan
    #acquisition.loc[acquisition['income']>acquisition['income'].mean()+3*acquisition['income'].std(),'income'] = np.nan

    # Spending Target Variables
    if targets_spend_file is not None:
        spend_train = targets_spend_file.copy()
        acquisition = acquisition.merge(spend_train.loc[spend_train['month']<=12,:].groupby('ids')['spends'].
                                                    mean().to_frame(name='target_spending').#apply(np.log1p).
                                                    astype(np.float32).reset_index(), 
                                                    how='left', on='ids')   
        #acquisition['target_spending'] = (acquisition['target_spending']/acquisition['credit_limit']).replace([np.inf,-np.inf],np.nan)
        acquisition['target_spending'] /= acquisition['reported_income'] 
        acquisition['target_fraud'] = acquisition['target_fraud'].notnull().astype(np.uint8)    
    
     #Log-Transformations
    log_cols = ['income', 'reported_income', 'credit_limit','last_amount_borrowed']
    for c in log_cols:
        acquisition['log_'+c] = np.log1p(acquisition[c])
    
    if targets_spend_file is not None:
        # Inflation Adjusted Values
        inflation_rate = 0.005
        targets_spend_file['spends'] = targets_spend_file['spends']/((1+targets_spend_file['month'])**inflation_rate)
        targets_spend_file['revolving_balance'] = targets_spend_file['revolving_balance']/((1+targets_spend_file['month'])**inflation_rate)    
        
    #Simple preprocessing:
    lat_lon = acquisition ['lat_lon'].fillna('(None,None)').apply(ast.literal_eval)
    places = rg.search([x for x in lat_lon if x[0] is not None]) 
    places_df = pd.DataFrame.from_dict(places).rename(columns={'admin1': 'estimated_state', 'name':'estimated_district'}).drop(['lat','lon','admin2','cc'],axis=1)
    places_df.index = [i for i,lat_lon in zip(acquisition.index, lat_lon) if lat_lon[0] is not None]
    places_df['estimated_state'] = places_df['estimated_state'].map(estimated_states_map)
    acquisition ['lat'] = [x[0] if x[0] is not None else np.nan for x in lat_lon.values]
    acquisition ['lon'] = [x[1] if x[1] is not None else np.nan for x in lat_lon.values]
    acquisition .drop('lat_lon', axis=1, inplace=True)
    acquisition  = acquisition.join(places_df, how='left')
    
    #Application Time
    acquisition['application_time_applied'] = acquisition['application_time_applied'].apply(lambda x: np.sum([int(m)*f for f,m in zip([60,1,1/60],x.split(":"))]))
    
    #email
    acquisition['email'] = acquisition['email'].replace('gmaill.com','gmail.com').replace('hotmaill.com','hotmail.com')
    
    # reported_income has inf values as observed in notebook 01_data_cleaning_eda.ipynb
    acquisition [QUANTITATIVE_VARS] = acquisition [QUANTITATIVE_VARS].replace(np.inf, np.nan)
    
    #User agent
    acquisition['shortned_user_agent']  = acquisition['user_agent'].str[:-7].astype('category')
    
    #zip region
    acquisition['shipping_state_zip_code'] = (acquisition['shipping_state'].astype(str)+acquisition['shipping_zip_code'].str[0]).astype('category')
    acquisition['shipping_zip_code'] = acquisition['shipping_zip_code'].apply(lambda x : str(x)[:2] if pd.isnull(x)==False else np.nan)
    
    #profile number
    acquisition['profile_is_cellphone'] = (acquisition['profile_phone_number'].str[4]=='9').astype('category')
    acquisition['profile_phone_number_ddd'] = acquisition['profile_phone_number'].apply(lambda x : str(x)[:2] if pd.isnull(x)==False else np.nan).astype('category')
        
    #external_data_provider_first_name
    acquisition['estimated_gender'] = acquisition['external_data_provider_first_name'].apply(lambda x : str(x)[-1]=='a' if pd.isnull(x)==False else np.nan).astype(np.uint8)
    acquisition['estimated_is_female'] = estimate_is_female(acquisition['external_data_provider_first_name'], data_path)
    acquisition['name_size'] = acquisition['external_data_provider_first_name'].apply(len)
    
    for c in QUALITATIVE_VARS:
        acquisition[c] = acquisition[c].astype("category")
    
    if targets_spend_file is not None:
        return acquisition, spend_train
    else:
        return acquisition

def estimate_is_female(names, data_path):
    db = pd.read_csv(os.path.join(data_path,'nomes_censo_2010.csv')).set_index('nome')
    return [np.round(db.loc[n].values[0]) if n in db.index else np.nan for n in names]

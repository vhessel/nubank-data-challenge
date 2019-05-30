import numpy as np
import os
import shutil

EXPERIMENT_FOLDERS = ['checkpoint','log','cv_results','final_validation']

def set_up_model(CONF):
    """ 
    Initial set-up before run an model
    """
    
    np.random.seed(CONF.get('random_seed'))
    
    model_path = CONF.get('model_path')
    
    if os.path.isdir(model_path) == False:        
            os.makedirs(CONF.get('model_path'))
            with open(os.path.join(model_path, 'random_seed.txt'),'w') as file:
                file.write(str(CONF.get('random_seed')))
    else:
        with open(os.path.join(model_path, 'random_seed.txt'),'r') as file:
            random_seed = int(file.read())
        assert random_seed == CONF.get('random_seed')

def set_up_experiment(EXP_CONF):
    """ 
    Initial set-up before run an experiment
    """
    if os.path.isdir(EXP_CONF.get('experiment_path')):
        #print("WARNING: The experiment " + experiment_name + " will be erased")
        #print("Ctrl+C to Stop or press any key to continue")
        #input()
        #shutil.rmtree(experiment_path)
        pass
    else:
        for f in EXPERIMENT_FOLDERS:
            os.makedirs(os.path.join(EXP_CONF.get('experiment_path'), f))
            
def get_experiment_conf(experiment_name, CONF):
    """
    Creates the Experiment configuration object used in the pipeline
    """
    EXP_CONF = CONF.get(experiment_name)
    EXP_CONF['model_name'] = CONF.get('model_name','unknown_model')
    EXP_CONF['name'] = experiment_name
    EXP_CONF['random_seed'] = CONF.get('random_seed')
    EXP_CONF['experiment_path'] = os.path.join(CONF.get('model_path'),experiment_name)
    EXP_CONF['data_path'] = CONF.get('data_path')
    EXP_CONF['test_size'] = CONF.get('test_size')
    return EXP_CONF
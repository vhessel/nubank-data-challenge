import click
import ast
import yaml
from src.pipeline_util import set_up_model, get_experiment_conf
from src.pipeline import GenericPipeline
import sys, traceback, ipdb

class PythonOptions(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if value.startswith("["):
                return ast.literal_eval(value)
            else:
                return [value]
        except:
            raise click.BadParameter(value)


@click.command()
@click.option('-d','--debug', is_flag=True)
@click.option('-m','--models', cls=PythonOptions, required=True)
@click.option('-a','--actions', cls=PythonOptions, default='', required=False)
def dispatcher(models, actions, debug):
    try:
        for m in models:
            CONF = yaml.load(open('config/' + m + '.yaml'))
            
            set_up_model(CONF)
                    
            experiments = CONF.get('experiments')
            for e in experiments:
                experiment_actions = CONF.get(e).get('actions')
                #Command line override
                if len(actions)>0:
                    experiment_actions = actions
                for a in experiment_actions:
                    pipeline = GenericPipeline(a, get_experiment_conf(e,CONF))
                
        #model_class = globals()[model.title().replace('_','') + 'Model']
        #obj = model_class(CONF)
    
    except:
        tp,val,tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)

if __name__ == "__main__":
        dispatcher()    
    
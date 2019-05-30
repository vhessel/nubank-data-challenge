import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

main_color = (97/255, 47/255, 116/255, 1.)

def plot_continuous_conditioned_variable(df, variable, condition, variable_name = 'True', max_bins = 8, ax = None):
    """ Plot a conditional distribution of a random variable conditioned to a continuous feature
    Parameters
    ----------
    df : pandas DataFrame 
        DataFrame with the columns indicated by the variable and condition parameters
    variable : string
        Name of column with the random variable data
    condition : string
        Name of the variable to be used in the conditional
    variable_name : string, optional
        Name of the random variable to be used in the barplots. Default is 'True'
    max_bins: int, optional
        Max number of bins to split the data. Default is 8
    ax : matplotlib Axos, optional
        Axes object to draw the plot onto, otherwise creates a new matplotlib figure
    """
    
    cleaned_data = df[[variable,condition]].dropna(how='any')
    
    h,b = np.histogram(cleaned_data[condition], bins = min(max_bins, cleaned_data[condition].unique().shape[0]))
    h = pd.Series(h)
    groups = np.array([np.where(x>=b)[0][-1] for x in cleaned_data[condition]])
    groups = np.minimum(groups,b.shape[0]-2)
    true_values = cleaned_data[[variable, condition]].groupby(by=groups)[variable].sum()
    count_values = cleaned_data[[variable, condition]].groupby(by=groups)[variable].count()
    true_values = true_values.reindex(h.index).fillna(0)
    count_values = count_values.reindex(h.index).fillna(0)

    true_values_norm = (true_values/h).fillna(0).to_frame().rename(columns={0: variable_name + ' Rate'})
    true_values_norm[condition] = np.round(b[1:],2)
    count_values = count_values.to_frame().rename(columns={variable: variable_name + ' Cases'})
    count_values[condition] = np.round(b[1:],2)
    
    if ax is None:
        fig = plt.figure(figsize=(9,7))
        ax = fig.add_subplot(111)
    
    bp = sns.barplot(data=true_values_norm, x=condition, y= variable_name + ' Rate', color=main_color, ax = ax)
    for index, row in true_values_norm.iterrows():
        bp.text(row.name,row[variable_name + ' Rate'], round(count_values[variable_name + ' Cases'].iat[index]), color='black', ha="center", va="bottom")
    plt.title('Conditioned ' + variable_name + ' Rate')
    
    
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
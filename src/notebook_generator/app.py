
# TODO
#from gui.mian_window import MainWindow
# def main():
#   app = MainWindow()
#   app.run

from core import notebook_builder
from i18n.manager import load_language
from core.parameters.NotebookConfig import NotebookConfig

output = 'C:/Users/raulr/OneDrive/Escritorio'
#dataset = 'C:/Users/raulr/machine learning/data/iris.csv'
dataset = 'C:/Users/raulr/machine learning/data/pima-indians-diabetes.csv'
target = 'final'
algorithms = ['Decision_tree']
title = None

_ = load_language('es')

#feature_columns=['Sepal.lenght', 'Sepal.width', 'Petal.lenght', 'Petal.width', 'class']
feature_columns=['preg','plas','pres','skin','test','mass','pedi','age','class']

#notebook config
Notebook = NotebookConfig(target_column='class',
                          feature_columns=feature_columns,
                          resume_plots=4,
                          type='regression',
                          normalizer='MinMaxScaler',
                          normalize_negative_data = ['pedi','age'])

multinotebook = {"one_file":True,
                 "describe":True,
                 "preprocessing":True}

notebook_builder.create_notebook(_, output, dataset, Notebook, multinotebook, title)

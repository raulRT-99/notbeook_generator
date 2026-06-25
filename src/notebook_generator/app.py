
# TODO
#from gui.mian_window import MainWindow
# def main():
#   app = MainWindow()
#   app.run

from core import notebook_builder
from i18n.manager import load_language
from core.parameters.NotebookConfig import NotebookConfig

output = 'C:/Users/raulr/OneDrive/Escritorio'
dataset = 'C:/Users/raulr/machine learning/data/pima-indians-diabetes.csv'
target = 'final'
algorithms = ['Decision_tree']
title = 'titulo del proyecto'

_ = load_language('es')

#notebook config
Notebook = NotebookConfig(target_column='class',
                          feature_columns=['preg','plas','pres','skin','test','mass','pedi','age','class'],
                          resume_plots=3)


notebook_builder.create_notebook(_, output, dataset, Notebook, title)

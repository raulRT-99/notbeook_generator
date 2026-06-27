# TODO
# from gui.mian_window import MainWindow
# def main():
#   app = MainWindow()
#   app.run

from core import notebook_builder
from i18n.manager import load_language
from src.notebook_generator.core.NotebookConfig import NotebookConfig

output = 'C:/Users/raulr/OneDrive/Escritorio'
target = 'final'
algorithms = ['Decision_tree']
title = None

_ = load_language('es')

data = {"reg": {
    "dataset": 'C:/Users/raulr/machine learning/data/housing.csv',
    "type": "regression",
    "features": ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO',
                 'B', 'LSTAT', 'class']
}, "class_int": {
    "dataset": 'C:/Users/raulr/machine learning/data/pima-indians-diabetes.csv',
    "type": "regression",
    "features": ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
}, "class_str": {
    "dataset": 'C:/Users/raulr/machine learning/data/iris.csv',
    "type": "regression",
    "features": ['Sepal.lenght', 'Sepal.width', 'Petal.lenght', 'Petal.width', 'class']}}

tipo = 'reg'

# notebook config
Notebook = NotebookConfig(target_column='class',
                          feature_columns=data.get(tipo).get('features'),
                          resume_plots=4,
                          type=data.get(tipo).get('type'),
                          normalizer='Normalizer')

multinotebook = {"one_file": True,
                 "describe": True,
                 "preprocessing": True,
                 "feature_selection": True}

notebook_builder.create_notebook(_, output, data.get(tipo).get('dataset'), Notebook, multinotebook, title)

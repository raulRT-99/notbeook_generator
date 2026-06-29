# TODO
# from gui.mian_window import MainWindow
# def main():
#   app = MainWindow()
#   app.run
import time

from core import notebook_builder
from i18n.manager import load_language
from src.notebook_generator.core.NotebookConfig import NotebookConfig
from src.notebook_generator.generators.algorithms.Knn import Knn

output = 'C:/Users/raulr/OneDrive/Escritorio'
target = 'final'
algorithms = ['Decision_tree']
title = None

_ = load_language('es')

data = {"reg": {
    "dataset": 'C:/Users/raulr/machine learning/data/housing.csv',
    "type": "regression",
    "features": ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO',
                 'B', 'LSTAT', 'class'],
    "separator": '\\s+'
}, "class_int": {
    "dataset": 'C:/Users/raulr/machine learning/data/pima-indians-diabetes.csv',
    "type": "classification",
    "features": ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class'],
    "separator": ","
}, "class_str": {
    "dataset": 'C:/Users/raulr/machine learning/data/iris.csv',
    "type": "classification",
    "features": ['Sepal.lenght', 'Sepal.width', 'Petal.lenght', 'Petal.width', 'class'],
    "separator": ','
}}

tipos = ['reg', 'class_int', 'class_str']

for tipo in tipos:
    # notebook config
    Notebook = NotebookConfig(target_column='class',
                              feature_columns=data.get(tipo).get('features'),
                              separator=data.get(tipo).get('separator'),
                              resume_plots=4,
                              type=data.get(tipo).get('type'),
                              normalizer='Normalizer')

    knn = Knn(name='knn', notebook=Notebook, parameters={"neighbors": "5"}, dataset=data.get(tipo).get('dataset'))

    multinotebook = {"one_file": True,
                     "describe": True,
                     "preprocessing": True,
                     "feature_selection": True}

    notebook_builder.create_notebook(_, output, data.get(tipo).get('dataset'), Notebook, multinotebook, [knn], tipo, )

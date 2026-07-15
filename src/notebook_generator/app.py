# TODO
# from gui.mian_window import MainWindow
# def main():
#   app = MainWindow()
#   app.run


from src.notebook_generator.gui.main_window import MainWindow

from i18n.manager import load_language
_ = load_language('es')

main = MainWindow(translator=_)
main.run()













# import time
#
# from core import notebook_builder
#
# from src.notebook_generator.core.NotebookConfig import NotebookConfig
# from src.notebook_generator.generators.algorithms.Knn import Knn
# from src.notebook_generator.generators.algorithms.Decision_tree import Decission_tree
# from src.notebook_generator.generators.algorithms.Gradient_boosting import Gradient_boosting
# from src.notebook_generator.generators.algorithms.Neuronal_network import Neural_network
# from src.notebook_generator.generators.algorithms.Random_forest import Random_forest
# from src.notebook_generator.generators.algorithms.SVM import SVM
#
# output = 'C:/Users/raulr/OneDrive/Escritorio/neva'
# target = 'final'
# algorithms = ['Decision_tree']
# title = None
#
#
#
# data = {"reg": {
#     "dataset": 'C:/Users/raulr/machine learning/data/housing.csv',
#     "type": "regression",
#     "features": ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO',
#                  'B', 'LSTAT', 'class'],
#     "separator": '\\s+'
# }, "class_int": {
#     "dataset": 'C:/Users/raulr/machine learning/data/pima-indians-diabetes.csv',
#     "type": "classification",
#     "features": ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class'],
#     "separator": ","
# }, "class_str": {
#     "dataset": 'C:/Users/raulr/machine learning/data/iris.csv',
#     "type": "classification",
#     "features": ['Sepal.lenght', 'Sepal.width', 'Petal.lenght', 'Petal.width', 'class'],
#     "separator": ','
# }}
#
# tipos = ['reg', 'class_int', 'class_str']
#
# for tipo in tipos:
#     # notebook config
#     Notebook = NotebookConfig(target_column='class',
#                               feature_columns=data.get(tipo).get('features'),
#                               separator=data.get(tipo).get('separator'),
#                               resume_plots=4,
#                               type=data.get(tipo).get('type'),
#                               normalizer='Normalizer')
#
#     knn = Knn(name='knn', notebook=Notebook, parameters={"neighbors": "5"}, dataset=data.get(tipo).get('dataset'))
#     dt = Decission_tree(name='Decission tree', notebook=Notebook, parameters={"test_size": "0.2", "random_state": "42"},
#                         dataset=data.get(tipo).get('dataset'))
#     gb = Gradient_boosting(name='Gradient boosting', notebook=Notebook,
#                            parameters={"test_size": "0.2", "random_state": "42"}, dataset=data.get(tipo).get('dataset'))
#     nn = Neural_network(name='Neural network', notebook=Notebook,
#                         parameters={"test_size": "0.2", "random_state": "42", "max_iter": "200",
#                                     "layer_size": "64,32,16"}, dataset=data.get(tipo).get('dataset'))
#     rf = Random_forest(name='Random forest', notebook=Notebook,
#                        parameters={"test_size": "0.2", "random_state": "42", "estimators": "100"},
#                        dataset=data.get(tipo).get('dataset'))
#     svm = SVM(name='SVM', notebook=Notebook,
#                        parameters={"test_size": "0.2", "random_state": "42", "C": "1.0"},
#                        dataset=data.get(tipo).get('dataset'))
#
#     multinotebook = {"one_file": True,
#                      "describe": True,
#                      "preprocessing": True,
#                      "feature_selection": True,
#                      "prediction": True}
#
#


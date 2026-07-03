from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.core_algorithm_process import core_algorithm_process


@dataclass
class Gradient_boosting(core_algorithm_process):

    def start_algorithm(self, _):
        super().start_algorithm(_)

    def import_dataset(self):
        self.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                               "from sklearn.model_selection import train_test_split\n"
                                               "from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor\n"
                                               "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error,mean_squared_error, r2_score\n"
                                               "filename = '" + self.dataset + "'\n"
                                                                               "names = " + self.columns + "\n"
                                                                                                           "df = pd.read_csv(filename,sep='" + self.notebook.separator + "', names=names)\n"
                                                                                                                                                                         "target_column = '" + self.notebook.target_column + "'\n"
                                                                                                                                                                                                                             "feature_columns = " + self.columns))

    def train_test_model(self):
        text_code = ("X = df.drop(columns=['" + self.notebook.target_column + "'])\n"
                     "y = df[target_column]\n\n"
                     "X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=" + self.parameters.get(
            'test_size') + ",random_state=" + self.parameters.get(
            'random_state') + ",stratify=y if y.value_counts().min() >= 2 else None)\n")

        if self.notebook.type == 'classification':
            text_code += "model = GradientBoostingClassifier(random_state=" + self.parameters.get('random_state') + ")"
        else:
            text_code += "model = GradientBoostingRegressor(random_state=" + self.parameters.get('random_state') + ")"

        self.cells.append(nbf.v4.new_code_cell(text_code))

    def results(self, _):
        text_code = ("model.fit(X_train, y_train)\n"
                     "y_pred = model.predict(X_test)\n\n")

        if self.notebook.type == 'classification':
            text_code += ("print('tradAccuracy:', accuracy_score(y_test, y_pred))\n"
                          "print(classification_report(y_test, y_pred))\n"
                          "print(confusion_matrix(y_test, y_pred))\n")
        else:
            text_code += ("print('MAE:', mean_absolute_error(y_test, y_pred))\n"
                          "print('MSE:', mean_squared_error(y_test, y_pred))\n"
                          "print('R2:', r2_score(y_test, y_pred))\n")

        self.cells.append(nbf.v4.new_code_cell(text_code))

    def predict(self, _):
        self.cells.append(nbf.v4.new_code_cell("nuevo_ejemplo = [[5, 120, 80, 32, 0, 35.5, 0.4, 45]]\n"
                                               "prediccion = model.predict(nuevo_ejemplo)\n"
                                               "print(prediccion[0])"))

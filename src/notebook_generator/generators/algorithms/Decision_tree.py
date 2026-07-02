from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.core_algorithm_process import core_algorithm_process


@dataclass
class Decission_tree(core_algorithm_process):

    def start_algorithm(self, _):
        super().start_algorithm(_)

    def import_dataset(self):
        columns = '[' + ', '.join(f"'{x}'" for x in self.notebook.feature_columns) + ']'
        self.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                               "from sklearn.model_selection import train_test_split\n"
                                               "from sklearn.pipeline import Pipeline\n"
                                               "from sklearn.preprocessing import StandardScaler\n"
                                               "from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor\n"
                                               "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_absolute_error, mean_squared_error, r2_score\n\n"
                                               "filename = '" + self.dataset + "'\n"
                                                                               "names = " + columns + "\n"
                                                                                                      "df = pd.read_csv(filename,sep='" + self.notebook.separator + "', names=names)\n"
                                                                                                                                                                    "target_column = '" + self.notebook.target_column + "'\n"
                                                                                                                                                                                                                        "feature_columns = " + columns))

    def train_test_model(self):
        text_code = ("X = df.drop(columns=['" + self.notebook.target_column + "'])\n"
                     "y = df[target_column]\n\n"
                     "X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=" + self.parameters.get(
            'test_size') + ",random_state=" + self.parameters.get(
            'random_state') + ",stratify=y if y.value_counts().min() >= 2 else None)\n")

        if self.notebook.type == 'classification':
            text_code += "model = DecisionTreeClassifier(random_state=" + self.parameters.get('random_state') + ")\n\n"
        else:
            text_code += "model = DecisionTreeRegressor(random_state=" + self.parameters.get('random_state') + ")\n\n"

        text_code += "model.fit(X_train, y_train)"

        self.cells.append(nbf.v4.new_code_cell(text_code))

    def results(self, _):
        if self.notebook.type == 'classification':
            self.cells.append(nbf.v4.new_code_cell("y_pred = model.predict(X_test)\n"
                                                   "print('-tradAccuracy:', accuracy_score(y_test, y_pred))\n"
                                                   "print(classification_report(y_test, y_pred))\n"
                                                   "print(confusion_matrix(y_test, y_pred))\n"))
        else:
            self.cells.append(nbf.v4.new_code_cell("y_pred = model.predict(X_test)\n"
                                                   "print('MAE:', mean_absolute_error(y_test, y_pred))\n"
                                                   "print('MSE:', mean_squared_error(y_test, y_pred))\n"
                                                   "print('R2:', r2_score(y_test, y_pred))"))

    def predict(self, _):
        self.cells.append(nbf.v4.new_code_cell("tradnuevo_ejemplo = [[5, 120, 80, 32, 0, 35.5, 0.4, 45]]\n"
                                               "prediccion = model.predict(nuevo_ejemplo)\n"
                                               "print(prediccion[0])"))

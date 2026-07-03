from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.core_algorithm_process import core_algorithm_process


@dataclass
class Knn(core_algorithm_process):

    def start_algorithm(self, _):
        super().start_algorithm(_)

    def import_dataset(self):
        # self.name
        columns = '[' + ', '.join(f"'{x}'" for x in self.notebook.feature_columns) + ']'
        self.cells.append(nbf.v4.new_markdown_cell('trad-'))
        self.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                               "from sklearn.model_selection import train_test_split\n"
                                               "from sklearn.pipeline import Pipeline\n"
                                               "from sklearn.preprocessing import StandardScaler\n"
                                               "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n\n"
                                               "filename = '" + self.dataset + "'\n"
                                                                               "names = " + columns + "\n"
                                                                                                      "df = pd.read_csv(filename,sep='" + self.notebook.separator + "', names=names)"))

    def train_test_model(self):

        text_code = ""
        if self.notebook.type == 'classification':
            text_code += "from sklearn.neighbors import KNeighborsClassifier\n"
        else:
            text_code += "from sklearn.neighbors import KNeighborsRegressor\n"

        text_code += ("target_column = '" + self.notebook.target_column + "'\n"
                                                                          "X = df.drop(columns=['" + self.notebook.target_column + "'])\n"
                                                                                                                                   "y = df['" + self.notebook.target_column + "']\n"
                                                                                                                                                                              "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)\n\n")

        if self.notebook.type == 'classification':
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('knn', KNeighborsClassifier(n_neighbors=" + self.parameters.get(
                'neighbors') + "))])\n\n")
        else:
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('knn', KNeighborsRegressor(n_neighbors=" + self.parameters.get(
                'neighbors') + "))])\n\n")

        text_code += "model.fit(X_train, y_train)"

        self.cells.append(nbf.v4.new_code_cell(text_code))

    def results(self, _):
        if self.notebook.type == 'classification':
            self.cells.append(nbf.v4.new_code_cell("y_pred = model.predict(X_test)\n\n"
                                                   "print('trad-Accuracy:', accuracy_score(y_test, y_pred))\n"
                                                   "print(classification_report(y_test, y_pred))\n"
                                                   "print(confusion_matrix(y_test, y_pred))\n"))
        else:
            self.cells.append(
                nbf.v4.new_code_cell("from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n\n"
                                     "y_pred = model.predict(X_test)\n"
                                     "print('R2:', r2_score(y_test, y_pred))\n"
                                     "print('MSE:', mean_squared_error(y_test, y_pred))\n"
                                     "print('MAE:', mean_absolute_error(y_test, y_pred))"))

    def predict(self, _):
        self.cells.append(nbf.v4.new_code_cell("new_values = [[5, 120, 80, 32, 0, 35.5, 0.4, 45]]\n"
                                               "prediction = model.predict(new_values)\n"
                                               "print('trad-Predicción: ', prediccion[0])"))

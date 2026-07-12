from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.base.core_algorithm_process import core_algorithm_process


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
                                                                                                                                                                              "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y if y.value_counts().min() >= 2 else None)\n\n")

        if self.notebook.type == 'classification':
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('knn', KNeighborsClassifier(n_neighbors=" + self.parameters.get(
                'neighbors') + "))])\n\n")
        else:
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('knn', KNeighborsRegressor(n_neighbors=" + self.parameters.get(
                'neighbors') + "))])\n\n")


        self.cells.append(nbf.v4.new_code_cell(text_code))

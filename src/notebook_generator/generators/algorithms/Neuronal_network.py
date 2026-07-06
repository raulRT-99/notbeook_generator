from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.core_algorithm_process import core_algorithm_process


@dataclass
class Neural_network(core_algorithm_process):

    def start_algorithm(self, _):
        super().start_algorithm(_)

    def import_dataset(self):
        self.cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                               "from sklearn.model_selection import train_test_split\n"
                                               "from sklearn.neural_network import MLPClassifier, MLPRegressor\n"
                                               "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix,mean_absolute_error, mean_squared_error, r2_score\n"
                                               "from sklearn.preprocessing import StandardScaler\n"
                                               "from sklearn.pipeline import Pipeline\n"
                                               "filename = '" + self.dataset + "'\n"
                                                                               "names = " + self.columns + "\n"
                                                                                                           "df = pd.read_csv(filename,sep='" + self.notebook.separator + "', names=names)\n"
                                                                                                                                                                         "target_column = '" + self.notebook.target_column + "'\n"
                                                                                                                                                                                                                             "feature_columns = " + self.columns))

    def train_test_model(self):
        size_list = [int(x) for x in self.parameters.get('layer_size').split(",")]
        size = '(' + ', '.join(f"{x}" for x in size_list) + ')'
        text_code = ("X = df.drop(columns=['" + self.notebook.target_column + "'])\n"
                                                                              "y = df[target_column]\n\n"
                                                                              "X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=" + self.parameters.get(
            'test_size') + ",random_state=" + self.parameters.get(
            'random_state') + ",stratify=y if y.value_counts().min() >= 2 else None)\n")

        if self.notebook.type == 'classification':
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('mlp', MLPClassifier(hidden_layer_sizes=" + size + ",activation='relu',max_iter=" + self.parameters.get(
                'max_iter') + ",random_state=" + self.parameters.get('random_state') + "))])")
        else:
            text_code += (
                    "model = Pipeline([('scaler', StandardScaler()),('mlp', MLPRegressor(hidden_layer_sizes=" + size + ",activation='relu',max_iter=" + self.parameters.get(
                'max_iter') + ",random_state=" + self.parameters.get('random_state') + "))])")

        self.cells.append(nbf.v4.new_code_cell(text_code))


from dataclasses import dataclass, field
from src.notebook_generator.core.NotebookConfig import NotebookConfig
import nbformat as nbf


@dataclass
class core_algorithm_process():
    name:str = ""
    notebook:NotebookConfig = None
    parameters:dict[str, str] = field(default_factory=dict)
    cells:list = field(default_factory=list)
    dataset:str = ""
    columns: str = ""

    def getColumnsString(self):
        self.columns = '[' + ', '.join(f"'{x}'" for x in self.notebook.feature_columns) + ']'

    def start_algorithm(self,_):
        self.getColumnsString()
        self.import_dataset()
        self.train_test_model()
        self.results(_)
        self.predict(_)


    def import_dataset(self):
        #name, imports, load_csv,
        pass

    def train_test_model(self):
        #target, train, test, model, fit
        pass

    def results(self, _):
        #evaluate
        text_code = ("model.fit(X_train, y_train)\n"
                     "y_pred = model.predict(X_test)\n\n")

        if self.notebook.type == 'classification':
            text_code += ("evaluation_matrix['"+self.name+"'] = accuracy_score(y_test, y_pred)\n\n"
                          "print('Accuracy:', accuracy_score(y_test, y_pred))\n"
                          "print(classification_report(y_test, y_pred))\n"
                          "print(confusion_matrix(y_test, y_pred))")
        else:
            text_code += ("MAE = mean_absolute_error(y_test, y_pred)\n"
                          "MSE = mean_squared_error(y_test, y_pred)\n"
                          "R2 = r2_score(y_test, y_pred)\n"
                          "evaluation_matrix['"+self.name+"'] = {'MAE': MAE, 'MSE': MSE, 'R2': R2}\n\n"
                          "print('MAE:', MAE)\n"
                          "print('MSE:', MSE)\n"
                          "print('R2:', R2)")

        self.cells.append(nbf.v4.new_code_cell(text_code))

    def predict(self, _):
        #predict new
        self.cells.append(nbf.v4.new_code_cell("new_dataset = [5, 120, 80, 32, 0, 35.5, 0.4, 45]  "+
                                               _("REPLACE-WITH-NEW-DATASET")+"\n"
                                               "prediccion = model.predict(new_dataset)\n"+
                                               "print(prediccion[0])"))
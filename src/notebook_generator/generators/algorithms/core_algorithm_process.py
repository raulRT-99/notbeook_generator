from dataclasses import dataclass, field
from src.notebook_generator.core.NotebookConfig import NotebookConfig


@dataclass
class core_algorithm_process():
    name:str = ""
    notebook:NotebookConfig = None
    parameters:dict[str, str] = field(default_factory=dict)
    cells:list = field(default_factory=list)
    dataset:str = ""

    def start_algorithm(self,_):
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
        pass

    def predict(self, _):
        #preccit new
        pass
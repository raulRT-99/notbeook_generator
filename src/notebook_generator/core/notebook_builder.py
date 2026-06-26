from pathlib import Path
import nbformat as nbf
from datetime import datetime
from src.notebook_generator.generators.decision_tree import generate_algorithm as DT
from src.notebook_generator.generators.knn import generate_algorithm as KNN
from src.notebook_generator.generators.random_forest import generate_algorithm as RF
from src.notebook_generator.core.resume import describe_dataset
from src.notebook_generator.core.preprocessing import preprocess_dataset
import os


def create_notebook(_, output_path, dataset, Notebook, multinotebook, title=None):
    if multinotebook.get('one_file'):
        nb = nbf.v4.new_notebook()
        nb = create_title_page(_, nb, Notebook.algorithms)
        if multinotebook.get('describe'):
            describe_process(dataset, Notebook.feature_columns, Notebook.target_column, Notebook.resume_plots,
                             Notebook.type, nb)
        if multinotebook.get('preprocessing'):
            preprocessing_process(nb, dataset, Notebook.feature_columns, Notebook.normalizer,
                                  Notebook.normalize_negative_data)
        # nb['cells'].extend(algorithms_process(_, Notebook.algorithms, dataset, Notebook.target_column))

        output_path = output_path + '/' + (title if title else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.ipynb'
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            nbf.write(nb, f)


def describe_process(dataset, feature_columns, target_column, resume_plots, type, nb):
    nb['cells'].extend(
        describe_dataset(dataset, feature_columns, target_column, resume_plots,
                         type))


def preprocessing_process(nb, dataset, features, normalizer, negative_data):
    nb['cells'].extend(preprocess_dataset(dataset, features, normalizer, negative_data))


def algorithms_process(_, algorithms, dataset, target_column):
    cells = []
    for algorithm in algorithms:
        match algorithm:
            case "Decision_tree":
                cells.extend(DT(_, dataset, target_column))
            case "K-nn":
                cells.extend(KNN(_, dataset, target_column))
            case "Random_forest":
                cells.extend(RF(_, dataset, target_column))
    return cells


def create_title_page(_, nb, algorithms):
    nb['cells'].append(nbf.v4.new_markdown_cell(_('trad-Portada notebook')))
    nb['cells'].append(nbf.v4.new_markdown_cell('## trad-algoritmos a analizar\n- ' + '\n- '.join(algorithms)))
    nb['cells'].append(nbf.v4.new_markdown_cell('trad-notas a tener en cuenta'))
    return nb

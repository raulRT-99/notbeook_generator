from pathlib import Path
import nbformat as nbf
from datetime import datetime
from src.notebook_generator.core.resume import describe_dataset
from src.notebook_generator.core.preprocessing import preprocess_dataset
from src.notebook_generator.generators.feature_selection import selection


def create_notebook(_, output_path, dataset, Notebook, multinotebook, algorithms, title=None):
    if multinotebook.get('one_file'):
        nb = nbf.v4.new_notebook()
        nb = create_title_page(_, nb, algorithms)
        if multinotebook.get('describe'):
            describe_process(_, dataset, Notebook.feature_columns, Notebook.target_column, Notebook.resume_plots,
                             Notebook.type, nb, Notebook.separator)
        if multinotebook.get('preprocessing'):
            preprocessing_process(_, nb, dataset, Notebook.feature_columns, Notebook.normalizer,
                                  Notebook.normalize_negative_data, Notebook.type, Notebook.target_column,
                                  Notebook.separator)
        if multinotebook.get("feature_selection"):
            nb['cells'].extend(
                selection(_, dataset, Notebook.feature_columns, Notebook.type, Notebook.target_column, Notebook.separator))

        nb['cells'].extend(algorithms_process(_, algorithms))

        output_path = output_path + '/' + (title if title else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.ipynb'
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", encoding="utf-8") as f:
            nbf.write(nb, f)


def describe_process(_,dataset, feature_columns, target_column, resume_plots, type, nb, separator):
    nb['cells'].append(nbf.v4.new_markdown_cell('trad-proceso de resumend e datos'))
    nb['cells'].extend(
        describe_dataset(_,dataset, feature_columns, target_column, resume_plots,
                         type, separator))


def preprocessing_process(_,nb, dataset, features, normalizer, negative_data, type, target, separator):
    nb['cells'].append(nbf.v4.new_markdown_cell('trad-proceso de preprocesamiento del dataset'))
    nb['cells'].extend(preprocess_dataset(_,dataset, features, normalizer, negative_data, type, target, separator))


def algorithms_process(_, algorithms):
    cells = []
    cells.append(nbf.v4.new_markdown_cell('trad---algorithms----'))
    for algorithm in algorithms:
        cells.append(nbf.v4.new_markdown_cell("-----------"+algorithm.name+"-----------"))
        algorithm.start_algorithm(_)
        cells.extend(algorithm.cells)
    return cells


def create_title_page(_, nb, algorithms):
    nb['cells'].append(nbf.v4.new_markdown_cell(_('trad-Portada notebook')))
    #nb['cells'].append(nbf.v4.new_markdown_cell('## trad-algoritmos a analizar\n- ' + '\n- '.join(algorithms.name)))
    nb['cells'].append(nbf.v4.new_markdown_cell('trad-notas a tener en cuenta'))
    return nb

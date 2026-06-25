from pathlib import Path
import nbformat as nbf
from datetime import datetime
from src.notebook_generator.generators.decision_tree import generate_algorithm as DT
from src.notebook_generator.generators.knn import generate_algorithm as KNN
from src.notebook_generator.generators.random_forest import generate_algorithm as RF


def create_notebook(_, output_path, dataset, Notebook, title = None):
    nb = nbf.v4.new_notebook()
    nb = create_title_page(_, nb, Notebook.algorithms)
    nb['cells'].extend(algorithms_process(_, Notebook.algorithms, dataset, Notebook.target_column))

    output_path = output_path + '/' + (title if title else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.ipynb'
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        nbf.write(nb, f)


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
    nb['cells'].append(nbf.v4.new_markdown_cell(_('Portada notebook')))
    nb['cells'].append(nbf.v4.new_markdown_cell('## algoritmos a analizar\n- '+'\n- '.join(algorithms)))
    nb['cells'].append(nbf.v4.new_markdown_cell('notas a tener en cuenta'))
    return nb
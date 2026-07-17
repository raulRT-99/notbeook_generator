from pathlib import Path
import nbformat as nbf
from datetime import datetime
from src.notebook_generator.core.resume import describe_dataset
from src.notebook_generator.core.preprocessing import preprocess_dataset
from src.notebook_generator.generators.feature_selection import selection
from src.notebook_generator.generators.evaluate import evaluate


def create_notebook(_, output_path, dataset, Notebook, multinotebook, algorithms, title=None):
    try:
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

            if multinotebook.get('prediction'):
                nb['cells'].append(nbf.v4.new_code_cell("evaluation_matrix = {}"))
                nb['cells'].extend(algorithms_process(_, algorithms))
                nb['cells'].extend(evaluate(_,Notebook.type))


            writeFile(output_path, title, nb)
        else:
            Path(output_path).mkdir(parents=True,exist_ok=True)
            x = 0
            if not title:
                title = str(x)

            if multinotebook.get('describe'):
                nb = nbf.v4.new_notebook()
                describe_process(_, dataset, Notebook.feature_columns, Notebook.target_column, Notebook.resume_plots,
                                 Notebook.type, nb, Notebook.separator)
                writeFile(output_path, title + '-describe', nb)
                if len(title) == 1:
                    x+=1
                    title = str(x)
            if multinotebook.get('preprocessing'):
                nb = nbf.v4.new_notebook()
                preprocessing_process(_, nb, dataset, Notebook.feature_columns, Notebook.normalizer,
                                      Notebook.normalize_negative_data, Notebook.type, Notebook.target_column,
                                      Notebook.separator)
                writeFile(output_path, title + '-preprocessing', nb)
                if len(title) == 1:
                    x += 1
                    title = str(x)
            if multinotebook.get("feature_selection"):
                nb = nbf.v4.new_notebook()
                nb['cells'].extend(
                    selection(_, dataset, Notebook.feature_columns, Notebook.type, Notebook.target_column,
                              Notebook.separator))
                writeFile(output_path, title + '-feature_selection', nb)
                if len(title) == 1:
                    x += 1
                    title = str(x)
            if multinotebook.get('prediction'):
                nb = nbf.v4.new_notebook()
                nb['cells'].extend(algorithms_process(_, algorithms))
                writeFile(output_path, title + '-prediction', nb)

    except TypeError:
        return {False:_("TYPE-ERROR-MSG")}
    except PermissionError:
        return {False:_("PERMISSION-ERROR-MSG")}
    except FileNotFoundError:
        return {False:_("FILE-NOT-FOUND-ERROR-MSG")}
    except OSError as e:
        return {False:_("OSERROR-MSG")}
    except Exception as e:
        return {False: _("UNEXPECTED-ERROR-MSG") % {"error": str(e)}}

    return {True:_("NOTEBOOK-GENERATED-MSG")}

def writeFile(output_path, title, nb):
    output_path = output_path + '/' + (title if title else datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.ipynb'
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        nbf.write(nb, f)


def describe_process(_,dataset, feature_columns, target_column, resume_plots, type, nb, separator):
    nb['cells'].append(nbf.v4.new_markdown_cell(_("DESCRIBE-PROCESS-TXT")))
    nb['cells'].extend(
        describe_dataset(_,dataset, feature_columns, target_column, resume_plots,
                         type, separator))


def preprocessing_process(_,nb, dataset, features, normalizer, negative_data, type, target, separator):
    nb['cells'].append(nbf.v4.new_markdown_cell(_("PREPROCESSING-PROCESS-TXT")))
    nb['cells'].extend(preprocess_dataset(_,dataset, features, normalizer, negative_data, type, target, separator))


def algorithms_process(_, algorithms):
    cells = []
    cells.append(nbf.v4.new_markdown_cell(_("ML-ALGORITHMS-PROCESS-TXT")))
    for algorithm in algorithms:
        cells.append(nbf.v4.new_markdown_cell("-----------"+algorithm.name+"-----------"))
        algorithm.start_algorithm(_)
        cells.extend(algorithm.cells)
    return cells


def create_title_page(_, nb, algorithms):
    nb['cells'].append(nbf.v4.new_markdown_cell(_("TITLE-PAGE")))
    nb['cells'].append(nbf.v4.new_markdown_cell(_("IMPORTANT-INFO-BREFORE-RUNING")))
    return nb

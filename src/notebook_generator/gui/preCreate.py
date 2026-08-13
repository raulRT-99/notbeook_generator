from src.notebook_generator.core.notebook_builder import create_notebook
from src.notebook_generator.core.NotebookConfig import NotebookConfig
from src.notebook_generator.generators.algorithms.Knn import Knn
from src.notebook_generator.generators.algorithms.Decision_tree import Decision_tree
from src.notebook_generator.generators.algorithms.Gradient_boosting import Gradient_boosting
from src.notebook_generator.generators.algorithms.Neuronal_network import Neural_network
from src.notebook_generator.generators.algorithms.Random_forest import Random_forest
from src.notebook_generator.generators.algorithms.SVM import SVM
from pathlib import Path


def onCreate(data, _):
    sep = None
    negative_features = []
    type = data.dataframe_type_map[data.dftype_cb.get()]
    target = data.target_feature.get() if data.target_feature.get() else '***TARGET COLUMN***'
    features = data.feature_names.get() if data.feature_names.get() else '***FEATURE COLUMNS***'
    features_list = features.split(',')

    if not data.output_name.get() or data.output_name.get().strip() == '':
        title = None
    else:
        title = data.output_name.get().strip()

    bool_dataset = not data.init_file.get() or data.init_file.get().strip() == ''
    if bool_dataset:
        dataset = '***PLEASE ADD A DATASET***'
    else:
        dataset = data.init_file.get().strip()

    bool_output = data.output_folder.get() or data.output_folder.get().strip() != ''
    if not bool_output and bool_dataset:
        output_folder = str(Path(data.init_file.get().strip()).parent)
    elif bool_output:
        output_folder = data.output_folder.get().strip()
    else:
        return {False: _("FOLDER-NOT-FOUND-ERROR")}

    if data.file_separator_str.get() or data.file_separator_str.get().strip() != '':
        sep = data.file_separator_str.get().strip()

    describe = data.describe_val.get()
    preprocess = data.preprocessing_val.get()
    negative_data = data.negative_data_val.get()
    if preprocess and negative_data:
        if data.negative_feature_names.get() or data.negative_feature_names.get().strip() != '':
            negative_features = data.negative_feature_names.get().strip().split(',')
        else:
            negative_data = False

    Notebook = NotebookConfig(target_column=target, feature_columns=features_list, type=type)
    if sep:
        Notebook.separator = sep
    if describe:
        Notebook.resume_plots = int(data.resume_plots_cb.get())
    if data.preprocessing_val.get():
        Notebook.normalizer = data.normalize_type_cb.get()
    if negative_data:
        Notebook.normalize_negative_data = negative_features

    ALGORITHM_CLASSES = {
        'K-Nearest Neighbors (KNN)': Knn,
        'Decision tree': Decision_tree,
        'Gradient Boosting': Gradient_boosting,
        'Neural Network': Neural_network,
        'Random forest': Random_forest,
        'Support-Vector Machines (SVM)': SVM
    }

    algorithms = [
        ALGORITHM_CLASSES[predict_param](
            name=predict_param,
            notebook=Notebook,
            parameters=data.predict_params[predict_param],
            columns=features,
            dataset=dataset,
        )
        for predict_param in data.predict_params.keys()
    ]

    multinotebook = {"one_file": not data.multinotebook_val.get(),
                     "describe": data.describe_val.get(),
                     "preprocessing": data.preprocessing_val.get(),
                     "feature_selection": data.feature_selection_val.get(),
                     "prediction": data.prediction_val.get()}

    return create_notebook(_, output_folder, dataset, Notebook, multinotebook=multinotebook,
                           algorithms=algorithms, title=title)

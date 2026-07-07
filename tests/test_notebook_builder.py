from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.notebook_generator.core.notebook_builder import create_notebook

class Test(TestCase):

    @patch("src.notebook_generator.core.notebook_builder.writeFile")
    @patch("src.notebook_generator.core.notebook_builder.evaluate")
    @patch("src.notebook_generator.core.notebook_builder.algorithms_process")
    @patch("src.notebook_generator.core.notebook_builder.selection")
    @patch("src.notebook_generator.core.notebook_builder.preprocessing_process")
    @patch("src.notebook_generator.core.notebook_builder.describe_process")
    @patch("src.notebook_generator.core.notebook_builder.create_title_page")
    def test_create_notebook_one_file(
            self,
            mock_title,
            mock_describe,
            mock_preprocessing,
            mock_selection,
            mock_algorithms_process,
            mock_evaluate,
            mock_writeFile
    ):
        mock_title.return_value = {"cells": []}
        mock_selection.return_value = []
        mock_algorithms_process.return_value = []
        mock_evaluate.return_value = []

        notebook = MagicMock()
        notebook.feature_columns = ["a", "b"]
        notebook.target_column = "class"
        notebook.resume_plots = False
        notebook.type = "clasification"
        notebook.normalizer = None
        notebook.normalize_negative_data = False
        notebook.separator = ","

        multinotebook = {
            "one_file": True,
            "describe": True,
            "preprocessing": True,
            "feature_selection": True,
            "prediction": True
        }

        create_notebook(
            _=None,
            output_path="salida",
            dataset="dataset",
            Notebook=notebook,
            multinotebook=multinotebook,
            algorithms=["knn"],
            title="mi_notebook"
        )

        mock_title.assert_called_once()
        mock_describe.assert_called_once()
        mock_preprocessing.assert_called_once()
        mock_selection.assert_called_once()
        mock_algorithms_process.assert_called_once()
        mock_evaluate.assert_called_once()
        mock_writeFile.assert_called_once()

    @patch("src.notebook_generator.core.notebook_builder.Path")
    @patch("src.notebook_generator.core.notebook_builder.writeFile")
    @patch("src.notebook_generator.core.notebook_builder.describe_process")
    def test_create_notebook_multi_file(self, mock_describe, mock_writeFile, mock_path):
        notebook = MagicMock()
        notebook.feature_columns = ["a", "b"]
        notebook.target_column = "class"
        notebook.resume_plots = False
        notebook.type = "clasification"
        notebook.normalizer = None
        notebook.normalize_negative_data = False
        notebook.separator = ","

        multinotebook = {
            "one_file": False,
            "describe": True,
            "preprocessing": False,
            "feature_selection": False,
            "prediction": False
        }

        create_notebook(
            _=None,
            output_path="salida",
            dataset="dataset",
            Notebook=notebook,
            multinotebook=multinotebook,
            algorithms=["knn"],
            title="mi_notebook"
        )

        mock_path.return_value.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_describe.assert_called_once()
        mock_writeFile.assert_called_once()
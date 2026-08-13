# Notebook Generator

- [Español](#español)
- [English](#english)

---

## Español

### Descripción

Notebook Generator es una aplicación de escritorio desarrollada en Python que permite crear notebooks de Jupyter personalizados a partir de datasets y configuraciones definidas por el usuario.

La aplicación facilita la preparación y generación de notebooks para proyectos de análisis de datos y aprendizaje automático. Permite seleccionar el archivo de datos, definir el separador de columnas, elegir las características y la variable objetivo, configurar el preprocesamiento, activar la selección automática de características y generar predicciones mediante distintos algoritmos de machine learning.

Además, Notebook Generator ofrece una interfaz gráfica configurable, soporte en inglés y español, personalización del tema y del tamaño de fuente, generación de notebooks independientes por fase del proceso y comprobación de nuevas versiones desde GitHub.

## Características

- Generación de notebooks de Jupyter a partir de datasets.
- Configuración de columnas, separadores y variable objetivo.
- Preprocesamiento y normalización de datos.
- Selección automática de características.
- Entrenamiento y predicción con algoritmos de machine learning.
- Soporte para español e inglés.
- Personalización del tema y del tamaño de fuente.
- Comprobación de nuevas versiones mediante GitHub.

---

## Requisitos

- Python 3.12 o superior.
- Dependencias incluidas en `requirements.txt`.

## Instalación

```bash
git clone https://github.com/raulRT-99/notebook_generator.git
cd notebook_generator
python -m pip install -r requirements.txt
```

## Ejecución
Para iniciar el proyecto es necesario arrancar desde el archivo app.py en src/notebook_generator/

```bash
python -m src.notebook_generator.app
```

## Uso

Para consultar el proceso completo de configuración y generación de notebooks, visita el manual de uso:

[Consultar el manual de uso en la Wiki](../../wiki)

## Estructura del proyecto

```text
notebook_generator/
├── src/
│   └── notebook_generator/
│       ├── Config/
│       ├── core/
│       ├── generators/
│       ├── gui/
│       ├── i18n/
│       └── app.py
├── tests/
├── requirements.txt
├── README.md
```

## Estado del proyecto

En desarrollo.

## Contribuciones

Las contribuciones, sugerencias y reportes de errores son bienvenidos. Para proponer cambios:

1. Crea un fork del repositorio.
2. Crea una rama para tus cambios.
3. Realiza un commit con una descripción clara.
4. Abre un Pull Request.

## Autor

Desarrollado por [raulRT99](https://github.com/raulRT-99).

## Licencia

Este proyecto se distribuye bajo la licencia [MIT License].

## English

### Description

Notebook Generator is a desktop application developed in Python that allows users to create customized Jupyter notebooks from datasets and user-defined configurations.

The application simplifies the preparation and generation of notebooks for data analysis and machine learning projects. It allows users to select the dataset file, define the column separator, choose the features and target variable, configure data preprocessing, enable automatic feature selection, and generate predictions using different machine learning algorithms.

Notebook Generator also provides a configurable graphical interface, support english and spanish, theme and font-size customization, the option to generate separate notebooks for each process phase, and version checking through GitHub.

## Features

- Jupyter notebook generation from datasets.
- Configuration of columns, separators, and target variables.
- Data preprocessing and normalization.
- Automatic feature selection.
- Training and prediction using machine learning algorithms.
- Support for Spanish and English.
- Theme and font-size customization.
- New version checking through GitHub.

---

## Requirements

- Python 3.12 or higher.
- Dependencies included in `requirements.txt`.

## Installation

```bash
git clone https://github.com/raulRT-99/notebook_generator.git
cd notebook_generator
python -m pip install -r requirements.txt
```

## Running the Application

To start the project, run the `app.py` module located in `src/notebook_generator/`:

```bash
python -m src.notebook_generator.app
```

## Usage

For the complete configuration and notebook-generation process, visit the user manual:

[View the user manual in the Wiki](../../wiki)

## Project Structure

```text
notebook_generator/
├── src/
│   └── notebook_generator/
│       ├── Config/
│       ├── core/
│       ├── generators/
│       ├── gui/
│       ├── i18n/
│       └── app.py
├── tests/
├── requirements.txt
├── README.md
```

## Project Status

In development.

## Contributing

Contributions, suggestions, and bug reports are welcome. To propose changes:

1. Fork the repository.
2. Create a branch for your changes.
3. Commit your changes with a clear description.
4. Open a Pull Request.

## Author

Developed by [raulRT99](https://github.com/raulRT-99).

## License

This project is distributed under the [MIT License](LICENSE).

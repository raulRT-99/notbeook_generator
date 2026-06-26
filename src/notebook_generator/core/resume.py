import math
import nbformat as nbf

def describe_dataset(dataset, features, target, plots, type):
    cells = []
    columns = '[' + ', '.join(f"'{x}'" for x in features) + ']'
    cells.extend(dataPreview(dataset, columns, target, type))
    if plots > 0:
        cells.extend(data_plots(features, plots, target, type))
    return cells


def dataPreview(dataset, columns, target, type):
    cells = []
    cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                      "filename = '" + dataset + "'\n"
                                                                 "names = " + columns + "\n"
                                                                                        "data = pd.read_csv(filename, names = names)\n"
                                                                                        "print(data)"))
    cells.append(nbf.v4.new_code_cell("data.head(15)"))
    cells.append(nbf.v4.new_code_cell("data.shape"))
    cells.append(nbf.v4.new_code_cell("data.dtypes"))
    cells.append(nbf.v4.new_code_cell("pd.set_option('display.width', 100)\n"
                                      "pd.set_option('display.precision', 3)\n"
                                      "data.describe()\n"))
    if type == 'classification':
        cells.append(nbf.v4.new_code_cell("data.groupby('" + target + "').size()"))
    else:
        cells.append(nbf.v4.new_code_cell("pd.set_option('display.width', 100)\n"
                                          "pd.set_option('display.precision', 3)\n"
                                          "correlation = data.corr(method='pearson')\n"
                                          "print(correlation)"))
        cells.append(nbf.v4.new_code_cell("data.skew()"))

    return cells


def data_plots(features, plots, target, type):
    cells = []
    fig_size = "16,10"
    if plots >= 1:
        cells.append(nbf.v4.new_code_cell("import matplotlib.pyplot as ptl\n"
                                          "fig = ptl.figure(figsize=(" + fig_size + "))\n"
                                                                                    "ax = fig.gca()\n"
                                                                                    "data.hist(ax = ax)\n"
                                                                                    "ptl.show()"))

    num_features = len(features) if type == 'regression' else len(features) - 1
    plot_cols = 4
    plot_rows = math.ceil(num_features / plot_cols)

    if plot_rows == 1:
        plot_cols = 2
        plot_rows = 2
    if plots >= 2:
        code_text = "import seaborn as sns\n" + "f, axes = ptl.subplots(" + str(plot_rows) + "," + str(
            plot_cols) + ", figsize = (" + fig_size + "))\n"
        index_col = 0
        for r in range(plot_rows):
            for c in range(plot_cols):
                if index_col >= num_features:
                    break
                if not (features[index_col] == target and type == 'classification'):
                    code_text += "sns.distplot(data['" + features[index_col] + "'], ax = axes[" + str(r) + "," + str(
                        c) + "])\n"
                index_col += 1

        cells.append(nbf.v4.new_code_cell(code_text))

    if plots >= 3:
        cells.append(nbf.v4.new_code_cell("fig = ptl.figure(figsize=(" + fig_size + "))\n"
                                                                                    "ax = fig.gca()\n"
                                                                                    "data.plot(ax = ax, kind = 'box', subplots = True, layout = (" + str(
            plot_cols) + "," + str(plot_rows) + "), sharex = False)\n"
                                                "ptl.show()"))

    if plots == 4 and type != 'classification':
        cells.append(nbf.v4.new_code_cell("import numpy as np\n"
                                          "correlations = data.corr()\n"
                                          "fig = ptl.figure()\n"
                                          "ax = fig.add_subplot(111) #el numero es un ID\n"
                                          "cax = ax.matshow(correlations, vmin=-1,vmax=1)\n"
                                          "fig.colorbar(cax)\n"
                                          "ticks = np.arange(0," + str(num_features) + ",1)\n"
                                                                                       "ax.set_xticks(ticks)\n"
                                                                                       "ax.set_yticks(ticks)\n"
                                                                                       "ax.set_xticklabels(names)\n"
                                                                                       "ax.set_yticklabels(names)\n"
                                                                                       "ptl.show()"))
        cells.append(nbf.v4.new_code_cell("correlation = data.corr()\n"
                                          "ptl.figure(figsize = (" + fig_size + "))\n"
                                                                                "ax = sns.heatmap(correlation, vmax = 1, square=True, annot=True, cmap = 'viridis')\n"
                                                                                "ptl.title('Matriz de correlacion')\n"
                                                                                "ptl.show()"))

    return cells

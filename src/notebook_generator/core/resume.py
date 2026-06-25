import math
import nbformat as nbf

def describe_dataset(dataset, features, target, plots, type):
    cells = []
    columns = '[' + ', '.join(f"'{x}'" for x in features) + ']'
    cells.extend(dataPreview(dataset,columns,target,type))
    if plots == 0:
        cells.extend(data_plots(features, plots, type))
    return cells


def dataPreview(dataset, columns, target, type):
    cells = []
    cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
        "filename = '"+dataset+"'\n"
        "names = "+columns+"\n"
        "data = pd.read_csv(filename, names = names)\n"
        "print(data)"))
    cells.append(nbf.v4.new_code_cell("data.head(15)"))
    cells.append(nbf.v4.new_code_cell("data.shape"))
    cells.append(nbf.v4.new_code_cell("data.dtypes"))
    cells.append(nbf.v4.new_code_cell("pd.set_option('display.width', 100)\n"
        "pd.set_option('display.precision', 3)\n"
        "data.describe()\n"))
    if type == 'classification':
        cells.append(nbf.v4.new_code_cell("data.groupby('"+target+"').size()"))
    cells.append(nbf.v4.new_code_cell("pd.set_option('display.width', 100)\n"
        "pd.set_option('display.precision', 3)\n"
        "correlation = data.corr(method='pearson')\n"
        "print(correlation)"))
    cells.append(nbf.v4.new_code_cell("data.skew()"))

    return cells

def data_plots(features, plots, type):
    cells= []
    if plots >= 1:
        cells.append(nbf.v4.new_code_cell("import matplotlib.pyplot as ptl\n"
            "fig = ptl.figure(figsize=(10,10))\n"
            "ax = fig.gca()\n"
            "data.hist(ax = ax)\n"
            "ptl.show()"))

    num_features = len(features)
    plot_cols = 4
    plot_rows = math.ceil(num_features / plot_cols)

    if plots >= 2:
        code_text = "import seaborn as sns\n"+"f, axes = ptl.subplots("+str(plot_cols)+","+str(plot_rows)+", figsize = (14,14))\n"
        index_col = 0
        for c in range(plot_cols):
            for r in range(plot_rows):
                code_text+= "sns.distplot(data['"+features[index_col]+"'], ax = axes["+str(c)+","+str(r)+"])\n"
                index_col+=1
                if index_col >= num_features:
                    break
        cells.append(nbf.v4.new_code_cell(code_text))

    if plots >= 3:
        cells.append(nbf.v4.new_code_cell("fig = ptl.figure(figsize=(14,14))\n"
            "ax = fig.gca()\n"
            "data.plot(ax = ax, kind = 'box', subplots = True, layout = ("+str(c)+","+str(r)+"), sharex = False)\n"
            "ptl.show()"))

    if plots == 4:
        cells.append("import numpy as np\n"
            "correlations = data.corr()\n"
            "fig = ptl.figure()\n"
            "ax = fig.add_subplot(111) #el numero es un ID\n"
            "cax = ax.matshow(correlations, vmin=-1,vmax=1)\n"
            "fig.colorbar(cax)\n"
            "ticks = np.arange(0,"+str(num_features)+",1)\n"
            "ax.set_xticks(ticks)\n"
            "ax.set_yticks(ticks)\n"
            "ax.set_xticklabels(names)\n"
            "ax.set_yticklabels(names)\n"
            "ptl.show()")
        cells.append(nbf.v4.new_code_cell("correlation = data.corr()\n"
            "ptl.figure(figsize = (10,10))\n"
            "ax = sns.heatmap(correlation, vmax = 1, square=True, annot=True, cmap = 'viridis')\n"
            "ptl.title('Matriz de correlacion')\n"
            "ptl.show()"))

    return cells
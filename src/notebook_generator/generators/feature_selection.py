import nbformat as nbf
import math
import pandas as pd


def selection(_,dataset, features, type, target, separator):
    cells = []
    columns = '[' + ', '.join(f"'{x}'" for x in features) + ']'
    num_features = len(features)
    target_string = False
    cells.append(nbf.v4.new_code_cell("import numpy as np\n"
                                      "import matplotlib.pyplot as plt\n"
                                      "import seaborn as sns\n"
                                      "import statsmodels.api as sm\n"
                                      "from sklearn.model_selection import train_test_split"))
    if type == 'classification':
        dataframe = pd.read_csv(dataset, names=features)
        if dataframe[target].dtype != 'int64':
            target_string = True

    if not target_string:
        cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                          "filename = '" + dataset + "'\n"
                                                                     "names = " + columns + "\n"
                                                                                            "dataframe = pd.read_csv(filename,sep='" + separator + "', names=names)\n"
                                                                                                                                                   "array = dataframe.values\n"
                                                                                                                                                   "X_df = array[:,0:" + str(
            num_features - 1) + "]\n"
                                "Y_df = array[:," + str(num_features - 1) + "]"))

    else:
        cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                          "import matplotlib.pyplot as plt\n"
                                          "import seaborn as sns\n\n"
                                          "filename = '" + dataset + "'\n"
                                                                     "names = " + columns + "\n"
                                                                                            "dataframe = pd.read_csv(filename, names=names)\n"
                                                                                            "X_df = dataframe.iloc[:, 0:4]\n"
                                                                                            "Y_df = dataframe.iloc[:, 4]"))

    cells.extend(correlation_plot(target_string))
    cells.extend(features_high_corr(target_string))
    if not target_string:
        cells.extend(backward_elimination())
    cells.extend(select_best(target_string))
    cells.extend(recursive_elimination(num_features, target_string))

    return cells


def correlation_plot(target_string):
    cells = []
    cells.append(nbf.v4.new_code_cell("plt.figure(figsize=(12,12))\n"
                                      "cor = " + ("dataframe" if not target_string else "X_df") + ".corr()\n"
                                                                                                  "sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)\n"
                                                                                                  "plt.show"))
    return cells


def features_high_corr(target_string):
    cells = []
    dataset = "dataframe" if not target_string else "X_df"
    cells.append(nbf.v4.new_code_cell("corr_matrix = " + dataset + ".corr().abs()\n"
                                                                   "upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool_))\n"
                                                                   "to_drop = [column for column in upper.columns if any(upper[column] > 0.75)]\n"
                                                                   "df_selected=" + dataset + ".drop(" + dataset + "[to_drop], axis=1)\n"
                                                                                                                   "df_selected"))
    cells.append(nbf.v4.new_code_cell("#trad-texto para decir si quiere un nuevo csv con la data preprocesada\n"
                                      "import os\n"
                                      "df_selected.to_csv('data_feature_selection.csv', index=False)"))
    return cells


def backward_elimination():
    cells = []
    cells.append(nbf.v4.new_code_cell("X_1 = sm.add_constant(X_df)\n"
                                      "model = sm.OLS(Y_df, X_1).fit()\n"
                                      "keep_indices = np.where(model.pvalues[1:] <= 0.05)[0]\n"
                                      "X_df_selected = X_df[:, keep_indices]\n"
                                      "X_df_selected"))
    cells.append(nbf.v4.new_code_cell("#trad-texto para decir si quiere un nuevo csv con la data preprocesada\n"
                                      "import os\n"
                                      "df_selected.to_csv('data_feature_selection.csv', index=False)"))
    return cells


def select_best(target_string):
    cells = []
    dataset = "dataframe" if not target_string else "X_df"
    text_code = ("from sklearn.feature_selection import SelectKBest\n"
                 "from sklearn.feature_selection import chi2\n\n"
                 "selector = SelectKBest(score_func=chi2, k=4)\n"
                 "fit = selector.fit(X_df, Y_df)\n"
                 "mask = fit.get_support()\n")
    if target_string:
        text_code += ("selected_cols = " + dataset + ".columns[mask]\n"
                                                     "df_selected = " + dataset + "[selected_cols]\n"
                                                                                  "df_selected = dataframe[selected_cols]\n"
                                                                                  "df_selected")
    else:
        text_code += ("feature_cols = dataframe.columns[0:8]\n"
                      "selected_cols = feature_cols[mask]\n"
                      "df_selected")
    cells.append(nbf.v4.new_code_cell(text_code))
    cells.append(nbf.v4.new_code_cell("#trad-texto para decir si quiere un nuevo csv con la data preprocesada\n"
                                      "import os\n"
                                      "df_selected.to_csv('data_feature_selection.csv', index=False)"))
    return cells


def recursive_elimination(num_features, target_string):
    cells = []
    percent_features = 0.6
    dataset = "dataframe" if not target_string else "X_df"
    text_code = ("from sklearn.feature_selection import RFE\n"
                 "from sklearn.linear_model import LogisticRegression\n\n"
                 "model = LogisticRegression(solver='lbfgs', max_iter=1000)\n"
                 "rfe = RFE(model, n_features_to_select=" + str(
        math.ceil(num_features * percent_features)) + ")\n"
                                                      "fit = rfe.fit(X_df, Y_df)\n")
    if target_string:
        text_code += ("selected_cols = " + dataset + ".columns[fit.support_]\n"
                                                     "df_selected = " + dataset + "[selected_cols]\n"
                                                                                  "df_selected")
    else:
        text_code += ("feature_cols = dataframe.columns[0:8]\n"
                      "selected_cols = feature_cols[mask]\n"
                      "df_selected = dataframe[selected_cols]\n"
                      "df_selected")
    cells.append(nbf.v4.new_code_cell(text_code))
    cells.append(nbf.v4.new_code_cell("#trad-texto para decir si quiere un nuevo csv con la data preprocesada\n"
                                      "import os\n"
                                      "df_selected.to_csv('data_feature_selection.csv', index=False)"))
    return cells

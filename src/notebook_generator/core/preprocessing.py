import nbformat as nbf
from src.notebook_generator.core.resume import data_plots


def preprocess_dataset(_,dataset, features, normalizer, negative_data, type, target, separator):
    cells = []
    columns = '[' + ', '.join(f"'{x}'" for x in features) + ']'
    num_features = len(features)
    cells.append(nbf.v4.new_code_cell("import pandas as pd\n"
                                      "import numpy as np\n"
                                      "import matplotlib.pyplot as plt\n"
                                      "import seaborn as sns\n\n"
                                      "filename = '" + dataset + "'\n"
                                                                 "names = " + columns + "\n"
                                                                                        "data = pd.read_csv(filename,sep='" + separator + "', names=names)\n"
                                                                                                                                          "array = data.values\n"
                                                                                                                                          "x = array[:, 0:" + str(
        num_features - 1) + "]\n"
                            "y = array[:, " + str(num_features - 1) + "]"))
    cells.extend(normalize(normalizer, negative_data, num_features))
    if negative_data:
        cells.extend(negative_data_normalize(negative_data))

    cells.append(nbf.v4.new_code_cell("data=df_scaled\n""df_data = data"))
    cells.extend(data_plots(features, 3, target, type))

    cells.append(nbf.v4.new_code_cell("#trad-texto para decir si quiere un nuevo csv con la data preprocesada\n"
                                      "import os\n"
                                      "df_data.to_csv('data_preprocessed.csv', index=False)"))

    return cells


def normalize(normalizer, negative_data, num_features):
    cells = []
    if normalizer == 'MinMaxScaler':
        text_code = ("from sklearn.preprocessing import MinMaxScaler\n"
                     "scaler = MinMaxScaler(feature_range=(0,1)) #escaladao de 0 a 1\n"
                     "rescaledX = scaler.fit_transform(x)\n\n")
    else:
        text_code = ("from sklearn.preprocessing import " + normalizer + "\n"
                                                                         "scaler = " + normalizer + "().fit(x)\n"
                                                                                                    "rescaledX = scaler.transform(x)\n")

    text_code += ("df_scaled = pd.DataFrame(rescaledX, columns=names[:" + str(num_features - 1) + "])\n"
                                                                                                  "df_scaled['class'] = y\n\n")
    if negative_data:
        text_code += "#trad-los valores negativos deben procesarse con yeo jhonnson\n\n"
        negative_columns = '[' + ', '.join(f"'{x}'" for x in negative_data) + ']'
        for ND in negative_data:
            text_code += "df_scaled.drop(['" + ND + "'], axis=1,inplace=True)\n"
        text_code += ("df_features = pd.DataFrame(data=data, columns = " + negative_columns + ")\n"
                                                                                              "df_scaled = pd.concat([df_features, df_scaled], axis=1)\n")
    text_code += "df_scaled.head()"
    cells.append(nbf.v4.new_code_cell(text_code))

    return cells


def negative_data_normalize(negative_data):
    cells = []
    negative_columns = '[' + ', '.join(f"'{x}'" for x in negative_data) + ']'
    text_code = ("#yeo=jhonson Transform, cuando hay valores negativos en el original\n"
                 "from sklearn.preprocessing import PowerTransformer\n"
                 "features = df_scaled[" + negative_columns + "]\n"
                                                              "pt = PowerTransformer(method='yeo-johnson', standardize=True)\n"
                                                              "skl_yeoj = pt.fit(features)\n"
                                                              "calc_lambdas = skl_yeoj.lambdas_\n"
                                                              "skl_yeoj = pt.transform(features)\n"
                                                              "df_features = pd.DataFrame(data=skl_yeoj, columns = " + negative_columns + ")\n"
                                                                                                                                          "df_features\n")

    for negative_c in negative_data:
        text_code += "df_scaled.drop(['" + negative_c + "'], axis=1,inplace=True)\n"
    cells.append(nbf.v4.new_code_cell(text_code))

    cells.append(nbf.v4.new_code_cell("df_data = pd.concat([df_scaled, df_features], axis=1)\n"
                                      "cols = df_data.columns.tolist()\n"
                                      "cols = cols[-1:] + cols[:-1]\n"
                                      "cols = cols[-1:] + cols[:-1]\n"
                                      "df_data = df_data[cols]\n"
                                      "df_data"))
    return cells

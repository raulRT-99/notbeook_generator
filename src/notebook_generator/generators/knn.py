import nbformat as nbf

def generate_algorithm(_, dataset, target_column,**kwargs):
    cells = []
    cells.append(nbf.v4.new_markdown_cell('Se realiza algoritmo de decision tree'))
    cells.append(nbf.v4.new_code_cell("print('hola mundo desde knn')"))
    return cells
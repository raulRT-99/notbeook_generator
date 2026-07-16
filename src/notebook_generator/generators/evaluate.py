import nbformat as nbf


def evaluate(_, type):
    return evaluateClassification(_) if type == 'classification' else evaluateRegresseion(_)


def evaluateClassification(_):
    cells = []
    cells.append(nbf.v4.new_code_cell("print('trad-algorithms comparison')\n\n"
                                      "for alg, acc in evaluation_matrix.items():\n"
                                      "\tprint(alg + ' -- ' + str(acc))"))
    return cells


def evaluateRegresseion(_):
    cells = []
    cells.append(nbf.v4.new_code_cell("print('trad-algorithms comparison\n')\n\n"
                                      "table = pd.DataFrame(evaluation_matrix).T\n"
                                      "print(table)"))
    return cells

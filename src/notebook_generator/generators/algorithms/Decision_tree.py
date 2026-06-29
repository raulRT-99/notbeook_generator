from dataclasses import dataclass
import nbformat as nbf

from src.notebook_generator.generators.algorithms.core_algorithm_process import core_algorithm_process


@dataclass
class Decission_tree(core_algorithm_process):




def generate_algorithm(_, dataset, target_column, **kwargs):
    cells.append(nbf.v4.new_code_cell("print('hola mundo desde decision tree')"))
    return cells

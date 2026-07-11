import random

KNN = {
    'parameters': [{
        'show_name': 'Neighbors',
        'back_name': 'neighbors',
        'option_type': 'combobox',
        'options': [3, 5, 7, 9],
        'default': 1
    }],
    'name': 'K-Nearest Neighbors (KNN)'
}

DT = {
    'parameters': [{
        'show_name': 'Test Size',
        'back_name': 'test_size',
        'option_type': 'incremental',
        'options': (0.1, 0.3, 0.05),
        'default': 0.2
    }, {
        'show_name': 'Random State',
        'back_name': 'random_state',
        'option_type': 'range',
        'options': (0, 400),
        'default': random.randint(0, 400)
    }],
    'name': 'Decision tree'
}

GB = {
    'parameters': [{
        'show_name': 'Test Size',
        'back_name': 'test_size',
        'option_type': 'incremental',
        'options': (0.1, 0.3, 0.05),
        'default': 0.2
    }, {
        'show_name': 'Random State',
        'back_name': 'random_state',
        'option_type': 'range',
        'options': (0, 400),
        'default': random.randint(0, 400)
    }],
    'name': 'Gradient Boosting'
}

NN = {
    'parameters': [{
        'show_name': 'Test Size',
        'back_name': 'test_size',
        'option_type': 'incremental',
        'options': (0.1, 0.3, 0.05),
        'default': 0.2
    }, {
        'show_name': 'Random State',
        'back_name': 'random_state',
        'option_type': 'range',
        'options': (0, 400),
        'default': random.randint(0, 400)
    }, {
        'show_name': 'Max Iter',
        'back_name': 'max_iter',
        'option_type': 'incremental',
        'options': (50, 500, 50),
        'default': 200
    }, {
        'show_name': 'Layer Size',
        'back_name': 'layer_size',
        'option_type': 'combobox',
        'options': ['8,4', '8,4,2', '16,8', '16,8,4', '32,16', '32,16,8', '64,32', '64,32,16', '64,32,16,8'],
        'default': 5
    }],
    'name': 'Neural Network'
}

RF = {
    'parameters': [{
        'show_name': 'Test Size',
        'back_name': 'test_size',
        'option_type': 'incremental',
        'options': (0.1, 0.3, 0.05),
        'default': 0.2
    }, {
        'show_name': 'Random State',
        'back_name': 'random_state',
        'option_type': 'range',
        'options': (0, 400),
        'default': random.randint(0, 400)
    }, {
        'show_name': 'Estimators',
        'back_name': 'estimators',
        'option_type': 'incremental',
        'options': (50, 500, 50),
        'default': 100
    }],
    'name': 'Random forest'
}

SVM = {
    'parameters': [{
        'show_name': 'Test Size',
        'back_name': 'test_size',
        'option_type': 'incremental',
        'options': (0.1, 0.3, 0.05),
        'default': 0.2
    }, {
        'show_name': 'Random State',
        'back_name': 'random_state',
        'option_type': 'range',
        'options': (0, 400),
        'default': random.randint(0, 400)
    }, {
        'show_name': 'C',
        'back_name': 'C',
        'option_type': 'combobox',
        'options': [0.01, 0.1, 1, 10, 100],
        'default': 2
    }],
    'name': 'Support-Vector Machines (SVM)'
}

ML_ALGORITHMS = [KNN, DT, GB, NN, RF, SVM]

# Constraints on obstacle positions
problems = {
    'left': [
        ((-1, 0), (-1, 1))
        ],
    'right': [
        ((0, 1), (-1, 1))
        ],
    'circle':  [
        ((0, 0), (0.5)),
        ],
    'balbis': [
        
    ],
    'einstein_tile': [
        
    ],
    'quarters': [
        ((-1, -0.375), (-0.375, 0.375)),
        ((-0.375, 0.375), (0.375, 1)),
        ((0.375, 1), (-0.375, 0.375)),
        ((-0.375, 0.375), (-1, -0.375)),
        ],
    'cross': [
        ((-0.1875, 0.1875), (0, 0.7)),
        ((-0.1875, 0.1875), (-0.7, 0)),
        ((-0.7, 0), (-0.1875, 0.1875)),
        ((0, 0.7), (-0.1875, 0.1875)),
        ],
    'corners': [
        ((1, 1), (1, 0.75), (0.75, 1)),
        ((1, -1), (1, -0.75), (0.75, -1)),
        ((-1, -1), (-1, -0.75), (-0.75, -1)),
        ((-1, 1), (-1, 0.75), (-0.75, 1)),
        ],
    }

def get_problem_list():
    return list(problems.keys())

def get_problem_instance(instance_name):
    instance_constr = problems[instance_name]
    return instance_constr
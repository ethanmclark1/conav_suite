# Constraints on obstacle positions
problems = {
    'corners': [
        ((1, 1), (1, 0.75), (0.75, 1)),
        ((1, -1), (1, -0.75), (0.75, -1)),
        ((-1, -1), (-1, -0.75), (-0.75, -1)),
        ((-1, 1), (-1, 0.75), (-0.75, 1)),
        ],
    'quarters': [
        ((-1, -0.375), (-0.375, 0.375)),
        ((-0.375, 0.375), (0.375, 1)),
        ((0.375, 1), (-0.375, 0.375)),
        ((-0.375, 0.375), (-1, -0.375)),
        ],
    'cross': [
        ((-0.1875, 0.1875), (0, 0.7)),
        ((-0.1875, 0.1875), (0, -0.7)),
        ((-0.7, 0), (-0.1875, 0.1875)),
        ((0.7, 0), (-0.1875, 0.1875)),
        ],
    'cluster':  [
        ((-0.50, 0.50), (-0.50, 0.50)),
        ],
    'left': [
        ((-1, 0), (-1, 1))
        ],
    'right': [
        ((0, 1), (-1, 1))
        ],
    'up': [
        ((-1, 1), (0, 1))
        ],
    'down': [
        ((-1, 1), (-1, 0))
        ],
    }

def get_problem_list():
    return list(problems.keys())

def get_problem_instance(instance_name):
    instance_constr = problems[instance_name]
    return instance_constr
# Constraints on obstalce positions
problems = {
    'v_cluster':  [
        ((-0.15, 0.15), (-0.15, 0.15)),
        ],
    'h_cluster': [
        ((-0.15, 0.15), (-0.15, 0.15))
        ],
    'v_wall': [
        ((-0.075, 0.075), (-0.6, 0.6))
        ],
    'h_wall': [
        ((-0.6, 0.6), (-0.075, 0.75))
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
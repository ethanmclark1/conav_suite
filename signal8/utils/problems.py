# Add more problems
problems = {
    'disaster_response_0': {
        'start': ((-0.05, 0.05), (-1, -0.90)),
        'goal': ((-0.85, -0.75), (0.90, 1)),
        'static_obs': (
            ((-1, -0.3), (0.30, 0.50)), 
            ((0.15, 0.40), (0.60, 1)), 
            ((-0.85, -0.75), (0.05, 0.15))
            ),
        'dynamic_obs': (((0.95, 1), (0.95, 1)),)
    },
    'disaster_response_1': {
        'start': ((-0.05, 0.05), (-1, -0.90)),
        'goal': ((0.80, 1), (-0.10, 0.10)),
        'static_obs': (
            ((-0.25, 0), (-0.3, 0.65)), 
            ((0.25, 0.45), (0.5, 1)), 
            ((0.75, 0.85), (-0.75, -0.30))
            ),
        'dynamic_obs': (((-0.6, -0.45), (0.95, 1)),)
        },
    # 'disaster_response_2': {},
    # 'disaster_response_3': {},
    # 'precision_farming_0': {},
    # 'precision_farming_1': {},
    # 'precision_farming_2': {},
    # 'precision_farming_3': {},
}

def get_problem_list():
    return list(problems.keys())

def get_problem(scenario_name):
    problem = problems[scenario_name]
    return problem
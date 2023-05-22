problems = {
    'v_cluster': {
        'start': ((-0.15, 0.15), (-1, -0.80)),
        'goal': ((-0.15, 0.15), (0.80, 1)),
        'static_obs': ((-0.15, 0.15), (-0.15, 0.15))
    },
    'h_cluster': {
        'start': ((-1, -0.80), (-0.15, 0.15)),
        'goal': ((0.80, 1), (-0.15, 0.15)),
        'static_obs': ((-0.15, 0.15), (-0.15, 0.15))
    },
    'v_wall': {
        'start': ((-1, 1), (-1, -0.80)),
        'goal': ((-1, 1), (0.80, 1)),
        'static_obs': ((-0.6, 0.6), (-0.075, 0.075))
    },
    'h_wall': {
        'start': ((-1, -0.80), (-1, 1)),
        'goal': ((0.80, 1), (-1, 1)),
        'static_obs': ((-0.075, 0.075), (-0.6, 0.6))
    },
    'left': {
        'start': ((0, 1), (-1, -0.80)),
        'goal': ((0, 1), (0.80, 1)),
        'static_obs': ((-1, 0), (-1, 1))
    },
    'right': {
        'start': ((-1, 0), (-1, -0.80)),
        'goal': ((-1, 0), (0.80, 1)),
        'static_obs': ((0, 1), (-1, 1))
    },
    'top': {
        'start': ((-1, -0.80), (-1, 0)),
        'goal': ((0.80, 1), (-1, 0)),
        'static_obs': ((-1, 1), (0, 1))
    },
    'bottom': {
        'start': ((-1, -0.80), (0, 1)),
        'goal': ((0.80, 1), (0, 1)),
        'static_obs': ((-1, 1), (-1, 0))
    },
}

def get_problem_list():
    return list(problems.keys())

def get_problem(scenario_name, dynamic_obstacles):
    static_scenario = problems[scenario_name]
    
    if dynamic_obstacles:
        dynamic_elements = {
            'v_cluster': {'dynamic_obs': (((-1, 1), (-0.45, -0.40)), ((-1, 1), (0.40, 0.45)))},
            'h_cluster': {'dynamic_obs': (((-0.45, -0.40), (-1, 1)), ((0.40, 0.45), (-1, 1)))},
            'v_wall': {'dynamic_obs': (((-1, 1), (-0.25, -0.20)), ((-1, 1), (0.20, 0.25)))},
            'h_wall': {'dynamic_obs': (((-0.45, -0.40), (-1, 1)), ((0.40, 0.45), (-1, 1)))},
            'left': {'dynamic_obs': (((-1, 1), (-0.40, -0.45)), ((-1, 1), (0.40, 0.45)))},
            'right': {'dynamic_obs': (((-1, 1), (-0.40, -0.45)), ((-1, 1), (0.40, 0.45)))},
            'top': {'dynamic_obs': (((-0.40, -0.45), (-1, 1)), ((0.40, 0.45), (-1, 1)))},
            'bottom': {'dynamic_obs': (((-0.40, -0.45), (-1, 1)), ((0.40, 0.45), (-1, 1)))},
        }
        dynamic_scenario = {**static_scenario, **dynamic_elements[scenario_name]}
        return dynamic_scenario
        
    return static_scenario
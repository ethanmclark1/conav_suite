import numpy as np

class NPC:
    def __init__(self):
        self.direction = None
        self.y_direction = 1
        self.status = 'moving_to_destination'
        self.farming_scenarios = {
            0: {'start': (0.9, -0.9), 'destination': (-0.8, -0.8), 'direction': 'left', 'bounds': [(-1, -0.4), (-1, 1)]},
            1: {'start': (0.9, -0.9), 'destination': (0.75, 0.75), 'direction': 'left', 'bounds': [(-1, 1), (0.4, 1)]},
            2: {'start': (-0.9, 0.2), 'destination': (-0.1875, -0.90), 'direction': 'right', 'bounds': [(-0.25, 0.25), (-1, 1)]},
            3: {'start': (-0.4, 0.9), 'destination': (-0.75, -0.80), 'direction': 'right', 'bounds': [(-1, 1), (-1, -0.4)]},
        }
    
    def get_scripted_action(self, obs, scenario_num):
        start = self.farming_scenarios[scenario_num]['start']
        destination = self.farming_scenarios[scenario_num]['destination']
        direction = self.farming_scenarios[scenario_num]['direction']
        bounds = self.farming_scenarios[scenario_num]['bounds']
        
        action = np.array([0, 0])
        x, y, = obs.state.p_pos
        
        if self.status == 'moving_to_destination':
            if np.allclose([x, y], destination, atol=0.05):
                self.status = 'zigzagging'
                self.direction = direction
            else:
                action = self._move_towards_point(x, y, destination)
        elif self.status == 'zigzagging':
            if self.y_direction == 1 and y > bounds[1][1] or self.y_direction == -1 and y < bounds[1][0]:
                self.status = 'moving_to_start'
            else:
                action = self._zigzag(x, y, bounds)
        elif self.status == 'moving_to_start':
            if np.allclose([x, y], start, atol=0.05):
                self.status = 'moving_to_destination'
            else:
                action = self._move_towards_point(x, y, start)

        return action
    
    def _move_towards_point(self, x, y, point):
            direction = np.array(point) - np.array([x, y])
            direction_norm = direction / np.linalg.norm(direction)
            return np.round(direction_norm).astype(int)

    def _within_bounds(self, x, y, bounds):
        x_bounds, y_bounds = bounds
        return x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]

    def _zigzag(self, x, y, bounds):
            if self.direction == 'right':
                if x < bounds[0][1]:
                    return np.array([1, 0])
                else:
                    self.direction = 'left' 
                    return np.array([0, self.y_direction])
            elif self.direction == 'left':
                if x > bounds[0][0]:
                    return np.array([-1, 0])
                else:
                    self.direction = 'right'
                    return np.array([0, self.y_direction])
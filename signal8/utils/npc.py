import numpy as np

class NPC:
    def __init__(self):
        self.direction = None
        self.status = 'moving_to_destination'
        self.farming_scenarios = {
            0: {"destination": (-0.8, -0.8), "direction": "left", 'bounds': [(-1, -0.4), (-1, 1)]},
            1: {"destination": (0.75, 0.75), "direction": "left", 'bounds': [(-1, 1), (0.4, 1)]},
            2: {"destination": (-0.1875, -0.90), "direction": "right", 'bounds': [(-0.25, 0.25), (-1, 1)]},
            3: {"destination": (-0.75, -0.80), "direction": "left", 'bounds': [(-1, 1), (-1, -0.4)]},
        }
    
    # TODO: Fix behavior 
    def get_scripted_action(self, obs, scenario_num):
        action = np.array([0, 0])
        start = obs.state.p_pos
        destination = self.farming_scenarios[scenario_num]['destination']
        direction = self.farming_scenarios[scenario_num]['direction']
        bounds = self.farming_scenarios[scenario_num]['bounds']
        x, y, = start
        
        if self.status == "moving_to_destination":
            if np.allclose([x, y], destination):
                self.status = "zigzagging"
                self.direction = direction  # Set initial direction
            else:
                action = self._move_towards_point(x, y, destination)
        elif self.status == "zigzagging":
            if not self._within_bounds(x, y, bounds):
                self.status = "moving_to_start"
            else:
                action = self._zigzag(x, y, bounds)
        elif self.status == "moving_to_start":
            if np.allclose([x, y], start):
                self.status = "moving_to_destination"
            else:
                action = self._move_towards_point(x, y, start)

        return action
    
    def _move_towards_point(self, x, y, point):
        direction = np.array(point) - np.array([x, y])
        direction_norm = direction / np.linalg.norm(direction)
        return direction_norm

    def _within_bounds(self, x, y, bounds):
        x_bounds, y_bounds = bounds
        return x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]

    # Zigzag within bounds like a lawn mower
    def _zigzag(self, x, y, bounds):
        if self.direction == "right":
            if x < bounds[0][1]:
                return np.array([1, 0])
            else:
                self.direction = "left" 
                return np.array([0, 1])
        elif self.direction == "left":
            if x > bounds[0][0]:
                return np.array([-1, 0])
            else:
                self.direction = "right"
                return np.array([0, 1])
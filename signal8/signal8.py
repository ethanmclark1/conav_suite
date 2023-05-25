import time
import threading
import numpy as np

from gymnasium.utils import EzPickle
from utils.scenario import BaseScenario
from utils.core import Agent, Landmark, DynamicObstacle, World
from utils.simple_env import SimpleEnv, make_env
from utils.problems import get_problem, get_problem_list

class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self, 
        agent_radius=0.1,
        goal_radius=0.05,
        num_obstacles=4,
        obstacle_radius=0.1,
        dynamic_obstacles=False,
        max_cycles=500, 
        continuous_actions=False, 
        render_mode="human"
        ):
        
        scenario = Scenario()
        world = scenario.make_world(
            agent_radius, 
            goal_radius,
            num_obstacles, 
            obstacle_radius, 
            dynamic_obstacles
            )
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=max_cycles, 
            continuous_actions=continuous_actions,
        )
        
        self.metadata["agent_radius"] = agent_radius
        self.metadata["goal_radius"] = goal_radius
        self.metadata["num_obstacles"] = num_obstacles
        self.metadata["obstacle_radius"] = obstacle_radius
        self.metadata["dynamic_obstacles"] = dynamic_obstacles

env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, agent_radius, goal_radius, num_obstacles, obstacle_radius, dynamic_obstacles):
        world = World(dynamic_obstacles)
        world.problem_scenarios = get_problem_list()
        
        self.scripted_obstacle_threads = []
        self.scripted_obstacle_running = False

        world.agents = [Agent() for _ in range(1)]
        for i, agent in enumerate(world.agents):
            agent.name = f"agent_{i}"
            agent.collide = True
            agent.size = agent_radius

        world.goals = [Landmark() for _ in range(len(world.agents))]
        for i, goal in enumerate(world.goals):
            goal.name = f"goal_{i}"
            goal.collide = False
            goal.size = goal_radius

        num_dynamic_obstacles = num_obstacles // 2 if dynamic_obstacles else 0
        world.obstacles = [DynamicObstacle() for _ in range(num_dynamic_obstacles)]
        world.obstacles += [Landmark() for _ in range(num_obstacles - num_dynamic_obstacles)]
        for i, obstacle in enumerate(world.obstacles):
            obstacle.name = f"obs_{i}"
            obstacle.size = obstacle_radius
                
        return world

    def reset_world(self, world, np_random, problem_name="v_cluster"):
        self.get_problem_scenario(world, problem_name)
        world.problem_name = problem_name
        
        # set state and color of both agents and goals
        for i, agent in enumerate(world.agents):
            agent.color = np.array([0, 0.8, 0])
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.p_pos = np_random.uniform(*zip(*world.start_constr))
            agent.goal = world.goals[i]
            agent.goal.color = np.array([0, 0, 0.8])
            agent.goal.state.p_vel = np.zeros(world.dim_p)
            agent.goal.state.p_pos = np_random.uniform(*zip(*world.goal_constr))
        
        # set state and color of obstacles
        for i, obstacle in enumerate(world.obstacles):
            if obstacle.movable:
                obstacle.color = np.array([0.5, 0, 0])
                obstacle.state.p_vel = np.zeros(world.dim_p)
                obstacle.state.p_pos = np.random.uniform(*zip(*world.dynamic_obstacle_constr[i % len(world.dynamic_obstacle_constr)]))
                obstacle.action_callback = self.get_scripted_action
            else:
                obstacle.color = np.array([0.2, 0.2, 0.2])
                obstacle.state.p_vel = np.zeros(world.dim_p)
                obstacle.state.p_pos = np_random.uniform(*zip(*world.static_obstacle_constr))  

        # Creates a new thread for each dynamic obstacle
        self.scripted_obstacle_running = True
        for obstacle in world.obstacles:
            if obstacle.movable:
                t = threading.Thread(target=self.run_scripted_obstacle, args=(world, obstacle,))
                t.start()
                self.scripted_obstacle_threads.append(t)   
    
    # Do not need to implement this function
    def reward(self, agent, world):
        return 0

    def observation(self, agent, world):
        return np.concatenate((agent.state.p_pos, agent.state.p_vel))
    
    def get_initial_state(self):
        a=3
    
    # Get constraints on entities given the problem name
    def get_problem_scenario(self, world, problem_name):
        problem = get_problem(problem_name, world.dynamic_obstacles)
        world.start_constr = problem['start']
        world.goal_constr = problem['goal']
        world.static_obstacle_constr = problem['static_obs']
        
        if world.dynamic_obstacles:
            world.dynamic_obstacle_constr = problem['dynamic_obs']
    
    # Get scripted action for adversarial agents s.t. they move in a straight line along their constraint
    def get_scripted_action(self, obs, world):
        action = np.zeros(world.dim_p)
        
        constr = world.dynamic_obstacle_constr[int(obs.name[-1])]
        constr_size = [(abs(point[0]) + abs(point[1])) for point in constr]
        dimension = 'horizontal' if constr_size[0] > constr_size[1] else 'vertical'

        # Always start off moving in the positive direction
        if dimension == 'horizontal':
            if (obs.state.p_vel == 0).all():
                action[0] = +1.0
            else:  # If moving, continue in the direction of velocity
                if obs.state.p_pos[0] <= constr[0][0]:  # If at left constraint, move right
                    action[0] = +1.0
                elif obs.state.p_pos[0] >= constr[1][0]:  # If at right constraint, move left
                    action[0] = -1.0
                else:  # Otherwise, follow the direction of velocity
                    action[0] = np.sign(obs.state.p_vel[0])
        else:
            if (obs.state.p_vel == 0).all():
                action[1] = +1.0
            else:  # If moving, continue in the direction of velocity
                if obs.state.p_pos[1] <= constr[0][1]:  # If at bottom constraint, move up
                    action[1] = +1.0
                elif obs.state.p_pos[1] >= constr[1][1]:  # If at top constraint, move down
                    action[1] = -1.0
                else:  # Otherwise, follow the direction of velocity
                    action[1] = np.sign(obs.state.p_vel[1])

        return action
    
    # Run a thread for each scripted obstacle
    def run_scripted_obstacle(self, world, obstacle):
        while self.scripted_obstacle_running:
            action = self.get_scripted_action(obstacle, world)
            sensitivity = 5.0
            obstacle.action = action * sensitivity
            obstacle.move()
            time.sleep(0.1)

    # Stop all threads for scripted obstacles
    def stop_scripted_obstacles(self):
        self.scripted_obstacle_running = False
        for t in self.scripted_obstacle_threads:
            t.join()
        self.scripted_obstacle_threads.clear()
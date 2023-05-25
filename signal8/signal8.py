import time
import threading
import numpy as np

from gymnasium.utils import EzPickle
from utils.scenario import BaseScenario
from utils.core import Agent, Goal, Obstacle, World
from utils.simple_env import SimpleEnv, make_env
from utils.problems import get_problem, get_problem_list

class raw_env(SimpleEnv, EzPickle):
    # TODO: Keep only essential parameters (i.e., remove radii)
    def __init__(
        self, 
        num_agents=1,
        num_obstacles=4,
        agent_radius=0.1,
        goal_radius=0.05,
        obstacle_radius=0.1,
        max_cycles=500, 
        render_mode="human"
        ):
        
        scenario = Scenario()
        world = scenario.make_world(
            num_agents,
            num_obstacles, 
            agent_radius, 
            goal_radius,
            obstacle_radius, 
            )
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=max_cycles, 
            continuous_actions=False,
        )
        
        # TODO: Verify if this is neccesary
        self.metadata["num_agents"] = num_agents
        self.metadata["num_obstacles"] = num_obstacles
        self.metadata["agent_radius"] = agent_radius
        self.metadata["goal_radius"] = goal_radius
        self.metadata["obstacle_radius"] = obstacle_radius

env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(
        self, 
        num_agents, 
        num_obstacles, 
        agent_radius, 
        goal_radius, 
        obstacle_radius, 
        ):
        
        world = World()
        world.problem_scenarios = get_problem_list()
        
        # TODO: Test out threading to see that it works correctly
        self.scripted_obstacle_threads = []
        self.obstacle_lock = threading.Lock()
        self.scripted_obstacle_running = False

        world.agents = [Agent() for _ in range(num_agents)]
        for i, agent in enumerate(world.agents):
            agent.name = f"agent_{i}"
            agent.collide = True
            agent.size = agent_radius

        world.goals = [Goal() for _ in range(len(world.agents))]
        for i, goal in enumerate(world.goals):
            goal.name = f"goal_{i}"
            goal.collide = False
            goal.size = goal_radius

        world.obstacles += [Obstacle() for _ in range(num_obstacles)]
        for i, obstacle in enumerate(world.obstacles):
            obstacle.name = f"obs_{i}"
            obstacle.size = obstacle_radius
                
        return world

    def reset_world(self, world, np_random, problem_name=None):
        if problem_name is None:
            problem_name = np_random.choice(world.problem_scenarios)
        self.get_problem_scenario(world, problem_name)
        
        # set state and color of both agents and goals
        for i, agent in enumerate(world.agents):
            agent.color = np.array([0, 0.8, 0])
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.p_pos = np_random.uniform(*zip(*world.start_constr))
            agent.goal = world.goals[i]
            agent.goal.color = np.array([0, 0, 0.8])
            agent.goal.state.p_vel = np.zeros(world.dim_p)
            agent.goal.state.p_pos = np_random.uniform(*zip(*world.goal_constr))
        
        num_dynamic_obs = len(world.dynamic_obstacle_constr)
        # set state and color of obstacles
        for i, obstacle in enumerate(world.obstacles):
            if i < num_dynamic_obs:
                obstacle.size = 0.025
                obstacle.movable = True
                obstacle.color = np.array([0.5, 0, 0])
                obstacle.state.p_vel = np.zeros(world.dim_p)
                obstacle.state.p_pos = np.random.uniform(*zip(*world.dynamic_obstacle_constr[i]))
                obstacle.action_callback = self.get_scripted_action
            else:
                obstacle.color = np.array([0.2, 0.2, 0.2])
                obstacle.state.p_vel = np.zeros(world.dim_p)
                obstacle.state.p_pos = np_random.uniform(*zip(*world.static_obstacle_constr[(i - num_dynamic_obs) % len(world.static_obstacle_constr)]))  

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
    
    # Get constraints on entities given the problem name
    def get_problem_scenario(self, world, problem_name):
        world.problem = get_problem(problem_name)
        world.problem_name = problem_name
        world.start_constr = world.problem['start']
        world.goal_constr = world.problem['goal']
        world.static_obstacle_constr = world.problem['static_obs']
        world.dynamic_obstacle_constr = world.problem['dynamic_obs']
    
    # TODO: Implement scripted actions for each problem
    """
    Disaster Response 0-1: Increase size of agent to resemble increasing severity of fire
    """
    def get_scripted_action(self, obs, world):
        action = np.zeros(world.dim_p)
        
        problem_name = world.problem_name
        if problem_name == 'disaster_response_0':
            obs.size *= 1.125
        elif problem_name == 'disaster_response_1':
            obs.size *= 1.050
        elif problem_name == 'disaster_response_2':
            obs.size *= 1.075
        elif problem_name == 'disaster_response_3':
            obs.size *= 1.075
        elif problem_name == 'precision_farming_0':
            action[0] = +1.0
        elif problem_name == 'precision_farming_1':
            action[0] = -1.0
        elif problem_name == 'precision_farming_2':
            action[0] = +1.0
        elif problem_name == 'precision_farming_3':
            action[0] = -1.0

        return action
    
    # Run a thread for each scripted obstacle
    def run_scripted_obstacle(self, world, obstacle):
        sensitivity = 5.0
        while self.scripted_obstacle_running:
            with self.obstacle_lock:
                action = self.get_scripted_action(obstacle, world)
                obstacle.action = action * sensitivity
                obstacle.move()
                time.sleep(0.1)

    # Stop all threads for scripted obstacles
    def stop_scripted_obstacles(self):
        self.scripted_obstacle_running = False
        for t in self.scripted_obstacle_threads:
            t.join()
        self.scripted_obstacle_threads.clear()
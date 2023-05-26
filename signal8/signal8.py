import time
import copy
import random
import threading
import numpy as np

from gymnasium.utils import EzPickle
from utils.scenario import BaseScenario
from utils.core import Agent, Goal, Obstacle, World
from utils.simple_env import SimpleEnv, make_env
from utils.problems import get_problem, get_problem_list

class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self, 
        num_agents=1,
        render_mode="human"):
        
        scenario = Scenario()
        world = scenario.make_world(num_agents)
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=500, 
            continuous_actions=False,
        )
        
env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, num_agents):
        world = World()
        world.problem_scenarios = get_problem_list()
        
        self.scripted_obstacle_threads = []
        self.scripted_obstacle_running = False

        world.agents = [Agent() for _ in range(num_agents)]
        for i, agent in enumerate(world.agents):
            agent.name = f"agent_{i}"
            agent.collide = True

        world.goals = [Goal() for _ in range(len(world.agents))]
        for i, goal in enumerate(world.goals):
            goal.name = f"goal_{i}"
            goal.collide = False
        
        # Minimum number of obstacles in a problem scenario 
        world.obstacles = [Obstacle() for _ in range(4)]
        for i, obstacle in enumerate(world.obstacles):
            obstacle.name = f"obs_{i}"
                
        return world
    
    # Get constraints on entities given the problem name
    def _set_problem_scenario(self, world, np_random, problem_name):
        if problem_name is None:
            problem_name = np_random.choice(world.problem_scenarios)
        problem_name = 'precision_farming_0'
        problem = get_problem(problem_name)
        world.problem_name = problem_name
        world.start_constr = problem['start']
        world.goal_constr = problem['goal']
        world.static_obstacle_constr = problem['static_obs']
        world.dynamic_obstacle_constr = problem['dynamic_obs']
    
    # Reset position of agent(s) and goal(s)
    def _reset_agents_and_goals(self, world, np_random):
        temp_start_constr = list(copy.copy(world.start_constr))
        temp_goal_constr = list(copy.copy(world.goal_constr))
        for i, agent in enumerate(world.agents):
            agent.color = np.array([0, 0.8, 0])
            agent.state.p_vel = np.zeros(world.dim_p)
            agent_constr = random.choice(temp_start_constr)
            agent.state.p_pos = np_random.uniform(*zip(*agent_constr))
            agent.start_pos = copy.copy(agent.state.p_pos)
            temp_start_constr.remove(agent_constr)

            agent.goal = world.goals[i]
            agent.goal.color = np.array([0, 0, 0.8])
            agent.goal.state.p_vel = np.zeros(world.dim_p)
            goal_constr = random.choice(temp_goal_constr)
            agent.goal.state.p_pos = np_random.uniform(*zip(*goal_constr))
            temp_goal_constr.remove(goal_constr)

        return temp_goal_constr
    
    # Reset position of dynamic obstacles
    def _reset_dynamic_obstacle(self, world, obstacle, np_random, temp_dynamic_obs_constr):
        obstacle.size = 0.025
        obstacle.movable = True
        obstacle.lock = threading.Lock()
        obstacle.color = np.array([0.5, 0, 0])
        obstacle.state.p_vel = np.zeros(world.dim_p)
        dynamic_obs_constr = random.choice(temp_dynamic_obs_constr)
        obstacle.state.p_pos = np_random.uniform(*zip(*dynamic_obs_constr))
        obstacle.action_callback = self.get_scripted_action
        temp_dynamic_obs_constr.remove(dynamic_obs_constr)

    # Reset position of static obstacles, taking leftover entities from goal constraints
    def _reset_static_obstacle(self, world, obstacle, np_random, temp_static_obs_constr):
        obstacle.color = np.array([0.2, 0.2, 0.2])
        obstacle.state.p_vel = np.zeros(world.dim_p)
        static_obs_constr = random.choice(temp_static_obs_constr)
        obstacle.state.p_pos = np_random.uniform(*zip(*static_obs_constr))  
        temp_static_obs_constr.remove(static_obs_constr)
    
    # Add or remove obstacles to match the number of obstacles in problem scenario
    def _match_obstacles_to_problem(self, world, num_static):
        num_total_obstacles = num_static + len(world.dynamic_obstacle_constr)
        if len(world.obstacles) > num_total_obstacles:
            world.obstacles = world.obstacles[:num_total_obstacles]
        elif len(world.obstacles) < num_total_obstacles:
            additional_obstacles = [Obstacle() for _ in range(len(world.obstacles), num_total_obstacles)]
            [setattr(obstacle, 'name', f"obs_{i+len(world.obstacles)}") for i, obstacle in enumerate(additional_obstacles)]
            world.obstacles.extend(additional_obstacles)
    
    # Reset position of obstacles
    def _reset_obstacles(self, world, np_random, leftover_entities):
        temp_static_obs_constr = list(copy.copy(world.static_obstacle_constr))
        temp_static_obs_constr += leftover_entities
        temp_dynamic_obs_constr = list(copy.copy(world.dynamic_obstacle_constr))
        
        num_dynamic_obs = len(temp_dynamic_obs_constr)
        self._match_obstacles_to_problem(world, len(temp_static_obs_constr))

        for i, obstacle in enumerate(world.obstacles):
            if i < num_dynamic_obs:
                self._reset_dynamic_obstacle(world, obstacle, np_random, temp_dynamic_obs_constr)
            else:
                self._reset_static_obstacle(world, obstacle, np_random, temp_static_obs_constr)
    
    # Start a thread for each dynamic obstacle
    def _start_scripted_obstacles(self, world):
        self.scripted_obstacle_running = True
        for obstacle in world.obstacles:
            if obstacle.movable:
                t = threading.Thread(target=self.run_scripted_obstacle, args=(world, obstacle,))
                t.start()
                self.scripted_obstacle_threads.append(t)   
    
    # TODO: Validate that this function works
    def reset_world(self, world, np_random, problem_name=None):
        self._stop_scripted_obstacles()
        self._set_problem_scenario(world, np_random, problem_name)
        leftover_entities = self._reset_agents_and_goals(world, np_random)
        self._reset_obstacles(world, np_random, leftover_entities)
        self._start_scripted_obstacles(world)
    
    # Do not need to implement this function
    def reward(self, agent, world):
        return 0

    def observation(self, agent, world):
        return np.concatenate((agent.state.p_pos, agent.state.p_vel))
        
    # TODO: Implement behavior for scripted obstacles
    """
    Disaster Response: Increase size of obstacle to resemble increasing size of fire/flood
    Precision Farming: Move obstacle in a zamboni pattern to resemble the tractor
    """
    def get_scripted_action(self, obs, world):
        action = np.zeros(world.dim_p)
        
        problem_name = world.problem_name
        if problem_name == 'disaster_response_0':
            obs.size *= 1.125
        elif problem_name == 'disaster_response_1':
            obs.size *= 1.100
        elif problem_name == 'disaster_response_2':
            obs.size *= 1.075
        elif problem_name == 'disaster_response_3':
            obs.size *= 1.050
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
            with obstacle.lock:
                action = self.get_scripted_action(obstacle, world)
                obstacle.action = action * sensitivity
                obstacle.move()
                time.sleep(0.1)

    # Stop all threads for scripted obstacles
    def _stop_scripted_obstacles(self):
        self.scripted_obstacle_running = False
        for t in self.scripted_obstacle_threads:
            t.join()
        self.scripted_obstacle_threads.clear()
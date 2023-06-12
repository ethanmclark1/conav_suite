import copy
import random
import numpy as np

# TODO
from utils.scenario import BaseScenario
from utils.simple_env import SimpleEnv, make_env
from utils.core import Agent, Goal, Obstacle, World
from utils.problems import get_problem_list, get_problem_instance

from gymnasium.utils import EzPickle


class raw_env(SimpleEnv, EzPickle):
    def __init__(self, num_agents=2, render_mode=None):
        if num_agents > 2:
            raise ValueError("Signal8 currently can only support up to 2 agents.")
        
        scenario = Scenario()
        world = scenario.make_world(num_agents)
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=500, 
        )
        
env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, num_agents):
        world = World()
        world.problem_list = get_problem_list()

        for i in range(num_agents):
            agent = Agent()
            agent.name = f"agent_{i}"
            agent.collide = True
            agent.color = np.array([1, 0.95, 0.8])
            world.agents.append(agent)
        
        # Agents has two goals (i.e., actual goal and start position)
        # This is to ensure agent returns safely to start position after reaching goal
        for i in range(num_agents*2):
            goal = Goal()
            goal.name = f"goal_{i}"
            goal.collide = False
            # goal_a is the actual goal
            if i < num_agents:
                goal.color = np.array([0.835, 0.90, 0.831])
            # goal_b is the start position to return to after reaching goal
            else:
                goal.color = np.array([0.85, 0.90, 0.99])
            world.goals.append(goal)
        
        for i in range(4):
            obstacle = Obstacle()
            obstacle.name = f"obs_{i}"
            obstacle.color = np.array([0.97, 0.801, 0.8])
            world.obstacles.append(obstacle)
        
        return world
    
    # Get constraints on entities given the problem instance name
    def _set_problem_instance(self, world, instance_name):
        instance_constr = get_problem_instance(instance_name)
        world.problem_instance = instance_name
        world.instance_constr = instance_constr
        
    # Reset obstacles to their initial positions
    def _reset_obstacles(self, world, np_random):
        for i, obstacle in enumerate(world.obstacles):            
            obstacle.state.p_vel = np.zeros(world.dim_p)
            idx = i % len(world.instance_constr)
            obstacle.state.p_pos = np_random.uniform(*zip(*world.instance_constr[idx]))
                    
    # Reset agents and goals to their initial positions
    def _reset_agents_and_goals(self, world, np_random):
        # Retrieve safe coordinates outside of the obstacles constraints
        x_constr = [constr[0] for constr in world.instance_constr]
        y_constr = [constr[1] for constr in world.instance_constr]
        def generate_safe_position():
            while True:
                x = np_random.uniform(-1, +1)
                y = np_random.uniform(-1, +1)
                if all(not (low <= x <= high) for low, high in x_constr) and all(not (low <= y <= high) for low, high in y_constr):
                    break
            return np.array([x, y])
        
        for i, agent in enumerate(world.agents):
            agent.state.p_vel = np.zeros(world.dim_p)
            agent.state.p_pos = generate_safe_position()
    
            agent.goal_a = world.goals[i]
            agent.goal_a.state.p_vel = np.zeros(world.dim_p)
            agent.goal_a.state.p_pos = generate_safe_position()
            
            agent.goal_b = world.goals[len(world.goals) - 1 - i]
            agent.goal_b.state.p_vel = np.zeros(world.dim_p)
            agent.goal_b.state.p_pos = copy.copy(agent.state.p_pos)
                        
    def reset_world(self, world, np_random, problem_instance):
        self._set_problem_instance(world, problem_instance)
        self._reset_obstacles(world, np_random)
        self._reset_agents_and_goals(world, np_random)
    
    # Reward given by agents to agents for reaching their respective goals
    def reward(self, agent, world):
        return 0
    
    def observation(self, agent, world):
        agent_pos = agent.state.p_pos
        agent_vel = agent.state.p_vel
        
        num_obstacles = len(world.obstacles)
        max_observable_dist = agent.max_observable_dist
        
        observed_obstacles = [np.full_like(agent_pos, max_observable_dist) for _ in range(num_obstacles)]
        observed_goal = np.full_like(agent_pos, max_observable_dist)
        
        for i, obstacle in enumerate(world.obstacles):
            obs_pos = obstacle.state.p_pos
            relative_pos = obs_pos - agent_pos
            dist = np.linalg.norm(relative_pos)
            if dist <= max_observable_dist:
                observed_obstacles[i] = relative_pos
                
        goal_pos = agent.goal_b.state.p_pos if agent.reached_goal else agent.goal_a.state.p_pos
        relative_goal_pos = goal_pos - agent_pos
        goal_dist = np.linalg.norm(relative_goal_pos)
        if goal_dist <= max_observable_dist:
            observed_goal = relative_goal_pos
        
        return np.concatenate((agent_pos, agent_vel, np.concatenate(observed_obstacles, axis=0), observed_goal))
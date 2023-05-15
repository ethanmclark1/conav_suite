import numpy as np

from gymnasium.utils import EzPickle
from utils.scenario import BaseScenario
from utils.core import Agent, Landmark, World
from utils.simple_env import SimpleEnv, make_env
from utils.problems import get_problem

class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self, 
        agent_radius=0.1,
        goal_radius=0.1,
        obs_radius=0.1,
        num_obstacles=4,
        has_dynamic_adversaries=False,
        max_cycles=500, 
        continuous_actions=False, 
        render_mode="human"
        ):
        
        scenario = Scenario()
        world = scenario.make_world(
            agent_radius, 
            goal_radius, 
            obs_radius, 
            num_obstacles, 
            has_dynamic_adversaries
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
        self.metadata["obs_radius"] = obs_radius
        self.metadata["num_obstacles"] = num_obstacles

env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, agent_radius, goal_radius, obs_radius, num_obstacles, has_dynamic_adversaries):
        world = World(has_dynamic_adversaries)
        
        world.agents = Agent()
        world.agents.name = "agent"
        world.agents.collide = False
        world.agents.silent = True
        world.agents.size = agent_radius
        
        world.landmarks = [Landmark() for _ in range(num_obstacles + 1)]
        world.landmarks[0].name = "goal"
        world.landmarks[0].collide = False
        world.landmarks[0].movable = False
        world.landmarks[0].size = goal_radius
        
        for i, landmark in enumerate(world.landmarks[1:]):
            landmark.name = f"obstacle_{i}"
            landmark.collide = False
            landmark.size = obs_radius
            if i >= num_obstacles // 2:
                landmark.movable = has_dynamic_adversaries
                
        return world

    def reset_world(self, world, np_random, problem_name="v_cluster"):
        # Agent is green, goal is blue, and obstacles are red
        world.agents.color = np.array([0.25, 0.75, 0.25])
        world.agents.goal = world.landmarks[0]
        world.agents.goal.color = np.array([0.25, 0.25, 0.75])
        for landmark in world.landmarks[1:]:
            landmark.color = np.array([0.75, 0.25, 0.25])
        
        self.get_problem_scenario(world, problem_name)
        
        world.agents.state.p_vel = np.zeros(world.dim_p)
        world.agents.state.p_pos = np_random.uniform(*zip(*world.start_constr))
        world.agents.goal.state.p_vel = np.zeros(world.dim_p)
        world.agents.goal.state.p_pos = np_random.uniform(*zip(*world.goal_constr))
        
        # set state of obstacles
        for i in range(len(world.landmarks[1:])):
            world.landmarks[i+1].state.p_vel = np.zeros(world.dim_p)
            world.landmarks[i+1].state.p_pos = np_random.uniform(*zip(*world.static_adversarial_constr))
    
    # Do not need to implement this function
    def reward(self, agent, world):
        return 0

    def observation(self, agent, world):
        return np.concatenate((agent.state.p_pos, agent.state.p_vel))
    
    def get_problem_scenario(self, world, problem_name):
        problem = get_problem(problem_name, world.has_dynamic_adversaries)
        world.start_constr = problem['start']
        world.goal_constr = problem['goal']
        world.static_adversarial_constr = problem['static_adversary']
        
        if world.has_dynamic_adversaries:
            world.dynamic_adversarial_constr = problem['dynamic_adversary']
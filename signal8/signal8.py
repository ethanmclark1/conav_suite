import math
import numpy as np

from gymnasium.utils import EzPickle
from .utils.scenario import BaseScenario
from .utils.core import Agent, Landmark, World, Action
from .utils.simple_env import SimpleEnv, make_env
from .utils.problems import get_problem, get_problem_list

class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self, 
        agent_radius=0.1,
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
        self.metadata["num_obstacles"] = num_obstacles
        self.metadata["obstacle_radius"] = obstacle_radius
        self.metadata["dynamic_obstacles"] = dynamic_obstacles

env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, agent_radius, num_obstacles, obstacle_radius, dynamic_obstacles):
        world = World(dynamic_obstacles)
        world.problem_scenarios = get_problem_list()
        
        num_dynamic_obstacles = math.floor(num_obstacles / 2) if dynamic_obstacles else 0
        num_agents = num_dynamic_obstacles + 1

        world.agents = [Agent() for _ in range(num_agents)]
        for i, agent in enumerate(world.agents):
            agent.adversary = True if i > 0 else False
            base_name = "adversary" if agent.adversary else "agent"
            base_index = i - 1 if agent.adversary else 0
            agent.name = f"{base_name}_{base_index}"
            agent.collide = False
            agent.silent = True
            agent.blind = agent.adversary
            agent.size = agent_radius
        
        world.landmarks = [Landmark() for _ in range(num_obstacles - num_dynamic_obstacles + 1)]
        world.landmarks[0].name = "goal_0"
        world.landmarks[0].collide = False
        world.landmarks[0].movable = False
        world.landmarks[0].size = agent_radius
        
        for i, landmark in enumerate(world.landmarks[1:]):
            landmark.name = f"obs_{i}"
            landmark.collide = False
            landmark.size = obstacle_radius
                
        return world

    def reset_world(self, world, np_random, problem_name="v_cluster"):
        self.get_problem_scenario(world, problem_name)
        world.problem_name = problem_name
        
        # set state and color of both agents and landmarks
        for i, agent in enumerate(world.agents):
            if agent.adversary:
                agent.color = np.array([0.5, 0, 0])
                agent.state.p_vel = np.zeros(world.dim_p)
                agent.state.p_pos = np_random.uniform(*zip(*world.dynamic_obstacle_constr[(i+1) % len(world.dynamic_obstacle_constr)]))
                agent.action_callback = self.get_scripted_action
            else:
                agent.color = np.array([0, 0.8, 0])
                agent.state.p_vel = np.zeros(world.dim_p)
                agent.state.p_pos = np_random.uniform(*zip(*world.start_constr))
                agent.goal = world.landmarks[0]
                agent.goal.color = np.array([0, 0, 0.8])
                agent.goal.state.p_vel = np.zeros(world.dim_p)
                agent.goal.state.p_pos = np_random.uniform(*zip(*world.goal_constr))
                
        for landmark in world.landmarks[1:]:
            landmark.color = np.array([0.2, 0.2, 0.2])
            landmark.state.p_vel = np.zeros(world.dim_p)
            landmark.state.p_pos = np_random.uniform(*zip(*world.static_obstacle_constr))
    
    # Do not need to implement this function
    def reward(self, agent, world):
        return 0

    def observation(self, agent, world):
        return np.concatenate((agent.state.p_pos, agent.state.p_vel))
    
    # Get constraints on entities given the problem name
    def get_problem_scenario(self, world, problem_name):
        problem = get_problem(problem_name, world.dynamic_obstacles)
        world.start_constr = problem['start']
        world.goal_constr = problem['goal']
        world.static_obstacle_constr = problem['static_obs']
        
        if world.dynamic_obstacles:
            world.dynamic_obstacle_constr = problem['dynamic_obs']
    
    # Get scripted action for adversarial agents s.t. they move in a straight line along their constraint
    def get_scripted_action(self, agent, world):
        action = Action()
        action.u = np.zeros(world.dim_p)
        action.c = np.zeros(world.dim_c)
        
        constr = world.dynamic_obstacle_constr(agent.name[-1])
        constr_size = [(abs(point[0]) + abs(point[1])) for point in constr]
        dimension = 'horizontal' if constr_size[0] > constr_size[1] else 'vertical'

        # Always start off moving in the positive direction
        if dimension == 'horizontal':
            if (agent.state.p_vel == 0).all():
                action.u[0] = +1.0
            else:  # If moving, continue in the direction of velocity
                if agent.state.p_pos[0] <= constr[0][0]:  # If at left constraint, move right
                    action.u[0] = +1.0
                elif agent.state.p_pos[0] >= constr[1][0]:  # If at right constraint, move left
                    action.u[0] = -1.0
                else:  # Otherwise, follow the direction of velocity
                    action.u[0] = np.sign(agent.state.p_vel[0])
        else:
            if (agent.state.p_vel == 0).all():
                action.u[1] = +1.0
            else:  # If moving, continue in the direction of velocity
                if agent.state.p_pos[1] <= constr[0][1]:  # If at bottom constraint, move up
                    action.u[1] = +1.0
                elif agent.state.p_pos[1] >= constr[1][1]:  # If at top constraint, move down
                    action.u[1] = -1.0
                else:  # Otherwise, follow the direction of velocity
                    action.u[1] = np.sign(agent.state.p_vel[1])

        return action
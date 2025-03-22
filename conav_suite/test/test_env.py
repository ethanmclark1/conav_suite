import conav_suite
import numpy as np


def print_separator(title: str) -> None:
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80)


def test_environment_creation() -> object:
    print_separator("Testing Environment Creation")
    
    print("Creating environment...")
    env = conav_suite.env()
    print("Environment created successfully")
    
    print("\nEnvironment properties:")
    print(f"  Version: {conav_suite.__version__}")
    
    return env


def test_environment_reset(env: object, problem_instance: str="bisect") -> np.ndarray:
    print_separator(f"Testing Environment Reset with '{problem_instance}'")
    
    print(f"Resetting environment with '{problem_instance}' problem instance...")
    env.reset(options={'problem_instance': problem_instance})
    print("Environment reset successfully")
    
    print("\nEnvironment state after reset:")
    print(f"  Agents: {env.agents}")
    print(f"  Current agent: {env.agent_selection}")
    
    # Get initial observation
    observation, reward, termination, truncation, info = env.last()
    print(f"\nInitial observation for {env.agent_selection}:")
    print(f"  Shape: {observation.shape}")
    print(f"  Value: {observation}")
    print(f"  Reward: {reward}")
    print(f"  Termination: {termination}")
    print(f"  Truncation: {truncation}")
    print(f"  Info: {info}")
    
    return observation


def test_action_observation_spaces(env: object) -> None:
    print_separator("Testing Action and Observation Spaces")
    
    agent = env.agent_selection
    action_space = env.action_space(agent)
    observation_space = env.observation_space(agent)
    
    print(f"Action space for {agent}:")
    print(f"  Type: {type(action_space)}")
    print(f"  Shape: {action_space.shape}")
    print(f"  Sample: {action_space.sample()}")
    
    print(f"\nObservation space for {agent}:")
    print(f"  Type: {type(observation_space)}")
    print(f"  Shape: {observation_space.shape}")
    print(f"  Low: {observation_space.low}")
    print(f"  High: {observation_space.high}")


def test_taking_steps(env: object, num_steps: int=5) -> None:
    print_separator(f"Testing Taking {num_steps} Steps")
    
    for step in range(num_steps):
        print(f"\nStep {step+1}:")
        agent = env.agent_selection
        action_space = env.action_space(agent)
        action = action_space.sample()
        
        print(f"  Agent: {agent}")
        print(f"  Action: {action}")
        
        env.step(action)
        observation, reward, termination, truncation, info = env.last()
        
        print(f"  New observation shape: {observation.shape}")
        print(f"  Reward: {reward}")
        print(f"  Termination: {termination}")
        print(f"  Truncation: {truncation}")
        
        # If episode ended, reset
        if termination or truncation:
            print("  Episode ended, resetting...")
            env.reset(options={'problem_instance': 'bisect'})


def test_all_problem_instances(env: object) -> None:
    print_separator("Testing All Problem Instances")
    
    # List of problem instances from the code
    problem_instances = [
        'bisect', 'circle', 'cross', 'corners', 
        'staggered', 'quarters', 'scatter', 'stellaris'
    ]
    
    for instance in problem_instances:
        print(f"\nTesting problem instance: {instance}")
        try:
            env.reset(options={'problem_instance': instance})
            print(f"Successfully reset with '{instance}'")
            
            # Take a random action to verify things work
            agent = env.agent_selection
            action = env.action_space(agent).sample()
            env.step(action)
            print(f"Successfully took action in '{instance}'")
            
        except Exception as e:
            print(f"Error with problem instance '{instance}': {e}")


def main() -> None:
    print_separator("CONAV_SUITE ENVIRONMENT TEST")
    print(f"Testing conav_suite version: {conav_suite.__version__}")
    
    try:
        env = test_environment_creation()
        
        test_environment_reset(env)
        
        test_action_observation_spaces(env)
        
        test_taking_steps(env)
        
        test_all_problem_instances(env)
        
        print_separator("Closing Environment")
        env.close()
        print("Environment closed successfully")
        
        print_separator("TEST COMPLETED SUCCESSFULLY")
        
    except Exception as e:
        print_separator("TEST FAILED")
        print(f"Error: {e}")
        
        try:
            if 'env' in locals():
                env.close()
                print("Environment closed despite error")
        except:
            pass


if __name__ == "__main__":
    main()
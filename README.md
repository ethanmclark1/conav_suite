# A Fork of Multi-Agent Particle Environment

Signal8 is an enhanced version of the Simple environment, originally developed by the [Farama Foundation](https://farama.org/) as part of their [Multi-Agent Particle Environment (MPE)](https://pettingzoo.farama.org/environments/mpe/).

# Signal8

Signal8 is an open-source research project devoted to facilitating the evolution of communication strategies in multi-agent systems. The project, drawing inspiration from real-world scenarios such as disaster response and precision farming, features a dynamic environment that elevates the principles of the Lewis signaling game. This unique setting serves as a testing ground for the advancement of robot-to-robot communication protocols.

Each problem set within Signal8 encompasses four distinct instances, with each one posing different constraints on the positioning of entities such as starting points, goals, and both static and dynamic obstacles. This dynamic feature fosters examination of communication strategies in diverse settings, enhancing the environment's realism and adaptability.

A notable characteristic of Signal8 is its incorporation of asymmetric information, whereby two types of agents – an 'eye in the sky' agent with global information and ground agents with only local information – operate simultaneously. This asymmetry replicates real-world situations, presenting challenges for the development of efficient communication strategies. It also provides intriguing prospects for the generation of context-dependent language and high-level directives.

In Signal8, both static and dynamic obstacles are present, creating further complexities for agents navigating through the environment. Static obstacles provide persistent barriers, while dynamic obstacles introduce predictable elements that can move or change over time. This complexity enriches the environment, making it an even more challenging and realistic platform for testing multi-agent communication strategies.

For more information on utilizing the environment API, please refer to the [PettingZoo API documentation](https://pettingzoo.farama.org/content/basic_usage/).

## Installation

```
git clone https://github.com/ethanmclark1/signal8.git
cd signal8
pip install -r requirements.txt
pip install -e .
```

## Usage

```
import Signal8

env = Signal8.env()
env.reset(options={"problem_instance": 0}))
observation, _, terminations, truncations, _ = env.last()
env.step(action)
env.close()
```

## List of Problem Instances

| Problem Instance |                 Visualization                 |
| :--------------: | :--------------------------------------------: |
|  ``corners``   | ![1686604788813](image/README/1686604788813.png) |
|   ``quarters``   | ![1686604799335](image/README/1686604799335.png) |
|    ``cross``    | ![1686604808540](image/README/1686604808540.png) |
|   ``cluster``   | ![1686604839072](image/README/1686604839072.png) |
|     ``left``     | ![1686604845732](image/README/1686604845732.png) |
|    ``right``    | ![1686604851758](image/README/1686604851758.png) |
|      ``up``      | ![1686604859851](image/README/1686604859851.png) |
|     ``down``     | ![1686604868138](image/README/1686604868138.png) |

Each of the colored regions represents an area where the respective entity can be instantiated. Blue regions are starting regions, yellow regions represent goal regions and in the case of precision farming, if a goal region is not generated in the yellow region then changes to a static obstacle region but this is not the case for disaster response, instead the region where the goal was not instantiated does not impact the episode at all, the light red regions represent static obstacles, and dark red regions represent dynamic obstacles.

In the case of disaster response, the dynamic obstacle does not move, instead it incrementally increases the obstacle radius to simulate a fire. In the precision farming case, the dynamic obstacle represents the behavior of a hockey rink ice cleaner moving in zig zags.

## Paper Citation

If you used this environment for your experiments or found it helpful, consider citing the following papers:

Environments in this repo:

<pre>
@article{lowe2017multi,
  title={Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments},
  author={Lowe, Ryan and Wu, Yi and Tamar, Aviv and Harb, Jean and Abbeel, Pieter and Mordatch, Igor},
  journal={Neural Information Processing Systems (NIPS)},
  year={2017}
}
</pre>

Original particle world environment:

<pre>
@article{mordatch2017emergence,
  title={Emergence of Grounded Compositional Language in Multi-Agent Populations},
  author={Mordatch, Igor and Abbeel, Pieter},
  journal={arXiv preprint arXiv:1703.04908},
  year={2017}
}
</pre>

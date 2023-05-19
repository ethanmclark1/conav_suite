# A Fork of Multi-Agent Particle Environment

Signal8 is an adapted version of the Simple environment, originally developed by the Farama Foundation as part of their [Multi-Agent Particle Environment (MPE)](https://pettingzoo.farama.org/environments/mpe/).

# Signal8

This repository contains a simple multi-agent environment with continuous observations and a discrete action space, inspired by the Lewis Signaling game. The environment incorporates basic simulated physics to create a scenario where agents must communicate and collaborate effectively to navigate around both static and dynamic obstacles to reach a goal.

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

env = Signal8.env(dynamic_obstacles=True)
env.reset(options={"problem_name": "v_cluster"}))
```

## List of Problem Scenarios

|     Names     | Description                                                                                                                                                                                          |
| :------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  `Cluster`  | The environment features a central square formed by four obstacles, with the start on the left and the goal on the right side.                                                                       |
|  `L-Shaped`  | The environment showcases a central L-shaped configuration of four obstacles, with the starting point on the left boundary and the goal situated at the inner elbow of the L.                        |
|  `Vertical`  | Four obstacles are aligned vertically in the environment's center, with the starting point on the left boundary and the goal on the right boundary.                                                  |
| `Horizontal` | Four obstacles are arranged in a horizontal line at the environment's midsection, with the start on the left boundary and the goal on the right boundary.                                            |
|    `Top`    | Four obstacles are placed at the top of the environment, while the start is situated in the bottom half on the left boundary and the goal is in the bottom half on the right boundary.               |
|   `Bottom`   | Four obstacles are placed at the bottom of the environment, while the start is situated in the top half on the left boundary and the goal is in the top half on the right boundary.                 |
|   `Right`   | Four obstacles are situated on the right side of the environment, with the start positioned in the left half along the bottom boundary and the goal located in the left half along the top boundary. |
|    `Left`    | Four obstacles are situated on the left side of the environment, with the start positioned in the right half along the bottom boundary and the goal located in the left half along the top boundary. |

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

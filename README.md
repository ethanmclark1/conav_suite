# A Fork of Multi-Agent Particle Environment

Sig8 is an adapted version of the Simple environment, originally developed by the Farama Foundation as part of their [Multi-Agent Particle Environment (MPE)](https://pettingzoo.farama.org/environments/mpe/).

# Sig8

This repository contains a simple multi-agent environment with continuous observations and a discrete action space, inspired by the Lewis Signaling game. The environment incorporates basic simulated physics to create a scenario where multiple agents must communicate and collaborate effectively to achieve their goals.

## Installation

```
git clone https://github.com/ethanmclark1/sig8.git
cd sig8
pip install -r requirements.txt
pip install -e .
```

## Usage

```
from sig8 import sig8

env = sig8.env(problem_type='vertical')
env.reset()
```

## List of Problem Scenarios

| Names        | Description                                                                                                                                                   |
| :--------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   `cluster`   | Four obstacles positioned in a square in the center of the environment, start is on the left side, and goal is on the right side                              |
|   `L-Shaped`   | Four obstacles positioned in a L in the center of the environment, start is on the left boundary and goal is on the inner elbow of the L                      |
|   `Vertical`   | Four obstacles positioned in a vertical line in the middle of the enviornment, start is on the left boundary, goal, is on the right boundary                  |
|  `Horizontal`  | Four obstacles positioned in a horizontal line in the middle of the enviornment, start is on the left boundary, goal, is on the right boundary                |
|     `Top`     | Four obstacles positioned in the top of the enviornment, start is in the bottom half on the left boundary, goal is in the bottom half on the right boundary |
|    `Bottom`    | Four obstacles positioned in the bottom of the enviornment, start is in the top half on the left boundary, goal is in the top half on the right boundary     |
|    `Right`    | Four obstacles positioned in the right of the enviornment, start is in the left half on the bottom boundary, goal is in left half on the top boundary      |
|     `Left`     | Four obstacles positioned in the left of the enviornment, start is in the right half on the bottom boundary, goal is in right half on the top boundary     |

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

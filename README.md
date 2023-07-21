# An Extension of Multi-Agent Particle Environment

Signal8 is an enhancement on top of the Simple environment, originally developed by the [Farama Foundation](https://farama.org/) as part of their [Multi-Agent Particle Environment (MPE)](https://pettingzoo.farama.org/environments/mpe/).

# Signal8

Signal8 is an open-source research project aimed advancing the development of communication strategies in multi-agent systems. The project proposes a unique environment that emphasizes the principles of the Lewis signaling game. This distinct setting serves as a testing ground for advancing robot-to-robot communication protocols.

Each problem set within Signal8 introduces different constraints on entity positioning such as start points, goals, and obstacles. This dynamic aspect encourages the investigation of communication strategies in diverse settings, enhancing the environment's adaptability and realism.

A notable characteristic of Signal8 is its incorporation of asymmetric information, whereby two types of agents – an 'eye in the sky' agent with global information and ground agents with only local information – operate simultaneously. This asymmetry replicates real-world situations, presenting challenges for the development of efficient communication strategies. It also provides intriguing prospects for the generation of context-dependent language and high-level directives.

In Signal8, obstacles are split into two categories: large obstacles that are observable exclusively by the aerial agents, and small obstacles which are observable to ground agents only. This distinct division introduces further complexity for agents navigating the environment. Large obstacles serve as barriers that define the structure of the environment, while small obstacles, appearing unpredictably within the vicinity of the ground agents. Both large and small obstacles remain stationary throughout the instance, adding an element of constant challenge to the environment. This multi-layered design richly expands the realism and complexity of the environment, making Signal8 a more demanding and intriguing platform for testing multi-agent communication strategies.

For additional information on utilizing the environment API, please refer to the [PettingZoo API documentation](https://pettingzoo.farama.org/content/basic_usage/).

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
env.reset(options={'problem_instance': 'einstein_tile'}))
observation, _, terminations, truncations, _ = env.last()
env.step(action)
env.close()
```

## List of Problem Instances

| Problem Instance |                 Visualization                 |
| :---------------: | :--------------------------------------------: |
|    ``bisect``    | ![1688231528499](image/README/1688231528499.png) |
|    ``circle``    | ![1688231542146](image/README/1688231542146.png) |
|   ``corners``    | ![1686604788813](image/README/1686604788813.png) |
|     ``cross``     | ![1686604808540](image/README/1686604808540.png) |
| ``einstein_tile`` | ![1688231581499](image/README/1688231581499.png) |
|   ``quarters``   | ![1688231597856](image/README/1688231597856.png) |
| ``solar_system`` | ![1688231626872](image/README/1688231626872.png) |
| ``right_arrows`` | ![1688231657789](image/README/1688231657789.png) |

The red zones denote regions where large obstacles can be spawned, while the remaining space (indicated in white) designates areas eligible for agent deployment, goal placement, and generation of small obstacles.

## Contributing

We welcome contributions to Signal8! If you're interested in contributing, you can do so in the following ways:

* **Bug Reports** : If you discover a bug when using Signal8, please submit a report via the issues tab. When submitting an issue, please do your best to include a detailed description of the problem and a code sample, if applicable.
* **Feature Requests** : If you have a great idea that you think would improve Signal8, don't hesitate to post your suggestions in the issues tab. Please be as detailed as possible in your explanation.
* **Pull Requests** : If you have made enhancements to Signal8, please feel free to submit a pull request. We appreciate all the help we can get to make Signal8 better!

## Support

If you encounter any issues or have questions about Signal8, please feel free to contact us. You can either create an issue in the GitHub repository or reach out to us directly at [eclark715@gmail.com](mailto:eclark715@gmail.com).

## License

Signal8 is open-source software licensed under the [MIT license](https://chat.openai.com/LINK_TO_YOUR_LICENSE).

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

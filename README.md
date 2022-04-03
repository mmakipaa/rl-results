# Evaluation of Basic Reinforcement Learning Algorithms

This repository contains a set of evaluation results for basic Reinforcement Learning (RL) algorithms.

Python implementation of evaluated RL methods can be found in https://github.com/mmakipaa/rl.

Results of test runs are presented as Jupyter notebooks in [notebooks](notebooks) folder.

Results have been created by running a test run based on yaml configuration file [configs](configs) folder for a given number of iterations:

```py
python run.py --environment <environment> --iterations <iterations> --configfile <filename>
```

The results of a test run have been saved to a report file in folder [testruns](testruns). Files are named as `<environment>_<filename>_<iterations>.pik`.

See [rl/README.md](https://github.com/mmakipaa/rl/blob/main/README.md) for more information.

Main branch of the repo contains executed notebooks with output and images. As the images are fairly large, the notebooks might not get rendered by GitHub renderer. Links to notebooks renderd by [nbviewer](https://nbviewer.org/) are provided below. Much smaller notebooks with no output can be found in `dev`-branch. 


The following notebooks are available:

## All agents

Presents a comparison of all implemented episodic methods (including full-episode and episode-based TD) using our simple blackjack implementation as a test environment. Each method is trained for one million episodes. See config file [all_agents.yaml](configs/all_agents.yaml).

nbviewer: [all_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/all_agents.ipynb)

## Batch agents

A evaluation of LSPI-LSTDQ batch method with different approximations of action-value function again using blackjack environment. We compare Fourier cosine basis, polynomial basis and simple tile coding. Each method is trained for maximum of 20 LSPI iterations. See config file [batch_agents.yaml](configs/batch_agents.yaml).

nbviewer: [batch_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/batch_agents.ipynb)

## FC alpha agents

An comparison of learning strategies for parameter _epsilon_ with on-policy TD(0) Sarsa using blackjack as a test environment. Strategies tested include inverse visit count, scaled visit count and scaled exponential decay. Each method is trained for 100.000 episodes. See config file [fc_alpha_agents.yaml](configs/fc_alpha_agents.yaml).

nbviewer: [fc_alpha_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/fc_alpha_agents.ipynb)

## MC epsilon agents

A comparison of learning strategies for parameter epsilon with on-policy Monte Carlo using our simple blackjack implementation as a test environment. Strategies tested include inverse visit count, scaled visit count and scaled exponential decay. See config file [mc_epsilon_agents.yaml](configs/mc_epsilon_agents.yaml).

Following notebook presents a similar analysis for Sarsa TD(0).

nbviewer: [mc_epsilon_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/mc_epsilon_agents.ipynb)

## Sarsa epsilon agents

A comparison of learning strategies for parameter _epsilon_ with TD(0) Sarsa using blackjack as a test environment. Strategies tested include inverse visit count, scaled visit count and scaled exponential decay. Each method is trained for 100.000 episodes. See config file [sarsa_epsilon_agents.yaml](configs/sarsa_epsilon_agents.yaml).

nbviewer: [sarsa_epsilon_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/sarsa_epsilon_agents.ipynb)

## Tabular agents

An test run of tabular learning methods. Again using blackjack as environment and learning for 100.000 episodes. See config file [tabular_agents.yaml](configs/tabular_agents.yaml).

nbviewer: [tabular_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/tabular_agents.ipynb)

## TD agents

An evaluation of temporal-difference methods using TD(0) updates: Q-learning, Sarsa and Expected Sarsa, and also three different approximate representations of action-value function trained with semi-gradient Sarsa; Fourier cosine basis, polynomial basis and simple tile coding. Again, we use blackjack as test environment and learn for 100.000 episodes. See config file [td_agents.yaml](configs/td_agents.yaml).

nbviewer: [td_agents.ipynb](https://nbviewer.org/github/mmakipaa/rl-results/blob/main/notebooks/td_agents.ipynb)

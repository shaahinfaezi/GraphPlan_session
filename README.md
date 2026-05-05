![GraphPlan]([<img width="1500" height="1000" alt="planning_graph" src="https://github.com/user-attachments/assets/930c2997-aa8b-47a6-94a8-bf1f99c1bd95" />
])

# AI Planning System - GraphPlan

## Overview

This project is a framework for AI planning in Python, dedicated to implementing the **GraphPlan** algorithm. The codebase provides the fundamental class structures for modeling domains, states, and actions. It serves as an excellent sandbox for understanding automated planning, building layered planning graphs, evaluating mutual exclusions, and recursively extracting valid action sequences to achieve specific goals.

## Features

- **GraphPlan Algorithm**: A complete implementation of the GraphPlan search logic (`GraphPlanner.py`). It orchestrates the expansion of the planning graph and searches for a valid plan once the goal conditions are met without being mutually exclusive.

- **Planning Graph Structure**: Constructs a comprehensive `PlanningGraph` consisting of alternating state and action levels. It handles the core complexity of computing and tracking mutual exclusions (mutexes) between competing actions and state propositions.

- **State and Action Modeling**: Uses modular classes (`Action`, `Predicate`, `State`, `Entity`) to define the preconditions, positive/negative effects, and rules that dictate how the environment changes when actions are applied.

- **Modular Domains & Problems**: The project includes ready-to-use environments representing classic AI planning scenarios:
  - **Blocks World Domain**
  - **Satellite Domain**
  - **Tire/Mechanic Domain**
  - **Cake Domain**

- **Graph Visualization**: Includes visualization tools (`GraphPlot.py`) to map out and plot the structure of the generated planning graph, making it easier to visualize the graph's expansion, levels, and connections over time.

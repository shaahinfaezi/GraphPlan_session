from queue import Queue

from Model.State import State
from Planners.Planner import Planner

"""
result is a list that stores the sequence of actions needed to reach the goal state, in case the planner finds a solution.

frontier is a queue data structure that stores the states that need to be expanded. It follows the First-In-First-Out (FIFO) rule, meaning that the first state that was added to the queue will be the first one to be explored.

visited is a set that stores all the states that have already been visited during the search process. If a state has already been visited, it will not be added to either the frontier or all_states again. This helps to prevent the algorithm from revisiting the same states multiple times and getting stuck in a loop

"""


class ForwardPlanner(Planner):
    def __init__(self, problem):
        super().__init__(problem)

    def search(self):
        frontier = Queue()
        visited = set()
        goal = self.problem.goal_state

        # Check if goal state is already reached
        if self.problem.initial_state.goal_test(goal):
            return []

        # Add initial state to frontier and visited set
        frontier.put(self.problem.initial_state)
        visited.add(self.problem.initial_state)
        while not frontier.empty():
            current_state = frontier.get()

            # Generate successor states
            successor_states = self.successor(current_state)

            for successor_state in successor_states:
                # If goal state is found, build solution and return
                if successor_state.goal_test(goal):
                    return successor_state.build_solution()

                # Add successor state to frontier and visited set
                if successor_state not in visited:
                    frontier.put(successor_state)
                    visited.add(successor_state)

        return []

    def successor(self, current_state: State) -> list[State]:
        result = []
        for action in self.problem.domain.actions:
            if action.is_applicable(current_state):
                new_literals = action.progress(current_state).literals                
                new_state = State(
                    action_name=action.action_name,
                    literals=list(new_literals)
                )                
                new_state.parent = current_state                
                result.append(new_state)
        return result

from queue import Queue

from Model.State import State
from Planners.Planner import Planner

"""
result is a list that stores the sequence of actions needed to reach the goal state, in case the planner finds a solution.

frontier is a queue data structure that states that need to be expanded. It follows the First-In-First-Out (FIFO) rule, meaning that the first state that was added to the queue will be the first one to be explored.

visited is a set that stores all the states that have already been visited during the search process. If a state has already been visited, it will not be added to either the frontier or all_states again. This helps to prevent the algorithm from revisiting the same states multiple times and getting stuck in a loop

"""


class BackwardPlanner(Planner):
    def __init__(self, problem):
        super().__init__(problem)

    def search(self):
        """
        Backward search from goal to initial state.
        Returns a plan that when executed from initial state reaches goal state.
        """
        frontier = Queue()
        visited = set()
        initial = self.problem.initial_state
        goal = self.problem.goal_state

        if goal.goal_test(initial):
            return []

        frontier.put(goal)
        visited.add(goal)

        while not frontier.empty():
            current_state = frontier.get()
            predecessor_states = self.predecessor(current_state)

            for predecessor_state in predecessor_states:
                # When all regressed goals fit in initial state, solution found
                if predecessor_state.literals.issubset(initial.literals):
                    plan = predecessor_state.build_solution()
                    plan.reverse()
                    return plan

                if predecessor_state not in visited:
                    frontier.put(predecessor_state)
                    visited.add(predecessor_state)

        return []

    def predecessor(self, current_state) -> list[State]:
        result = []
        for action in self.problem.domain.actions:
            if action.is_relevant(current_state):
                regressed_state = action.regress(current_state)
                regressed_state.parent = current_state
                regressed_state.action_name = action.action_name
                result.append(regressed_state)
        return result
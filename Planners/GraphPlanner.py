from PlanningGraph.PlanningGraph import PlanningGraph
from Planners.Planner import Planner

from itertools import combinations

class GraphPlanner(Planner):
    """GraphPlan Algorithm: Forward expansion until goal is reachable, then backward search for solution."""
    
    def __init__(self, problem):
        super().__init__(problem)
        self.planning_graph = PlanningGraph(problem)
        # Memoization: store failed goal sets to avoid redundant search
        self.nogoods = set()

    def search(self):
        """
        Main GraphPlan loop:
        1. Expand graph (add action level + state level)
        2. Check if goals are achievable (no mutexes between them)
        3. If yes, extract solution via backward search
        4. If graph levels off with no solution, return None
        """
        goals = self.planning_graph.goal
        
        while True:
            # Check if all goals appear in current state level without mutexes
            if self.planning_graph.check_goal_achievable(goals):
                last_level_idx = len(self.planning_graph.levels) - 1
                # Try to find a valid plan using backward search
                solution = self.extract_solution(goals, last_level_idx)
                if solution is not None:
                    return solution
            
            # If graph hasn't changed, no solution exists
            if self.planning_graph.has_levelled_off():
                return None
                
            # Expand graph by one more level
            self.planning_graph.expand_graph()

    def extract_solution(self, goals, level_index):
        """
        Backward search: from state level, find actions that achieve goals.
        Recursively solve for the preconditions of those actions.
        
        Args:
            goals: set of (Predicate, is_positive) tuples to achieve
            level_index: current state level in the graph
            
        Returns:
            A plan (list of action steps) or None if no solution exists
        """
        # Base case: reached initial state
        if level_index == 0:
            return []
        
        # Memoization: if we've already failed at this level with this goal set, skip
        if (level_index, frozenset(goals)) in self.nogoods:
            return None
        
        # Get the action layer just before this state level
        action_layer = self.planning_graph.levels[level_index - 1]
        # Find all conflict-free action sets that satisfy the goals
        possible_action_sets = self.get_backward_actions(goals, action_layer)
        
        # Try each possible action set
        for action_set in possible_action_sets:
            
            new_goals = set()



            #Complete getting new goals
            ...
            
            # find plan_prefix
            plan_prefix = ...

            
            if plan_prefix is not None:
                # Filter out persistence actions (no-ops) from the solution
                step = [a.name for a in action_set if not a.name.startswith("Persist")]
                if step:
                    return plan_prefix + [step]
                else:
                    return plan_prefix
        
        # No valid action set found, record this as a nogood
        self.nogoods.add((level_index, frozenset(goals)))
        return None

    def get_backward_actions(self, goals, action_layer):
        """
        Find all conflict-free action sets that satisfy the goals.
        
        Steps:
        1. Find relevant actions: those that add/delete at least one goal
        2. Try all combinations of relevant actions
        3. Check if the combination covers all goals
        4. Check if actions don't have mutexes between them
        5. Return valid action sets
        """


        # Step 1: Filter actions that are relevant to at least one goal
        relevant_actions = []
        for action in action_layer.actions:
            for goal in goals:
                pred, is_positive = goal
                # Check if this action can help achieve this goal
                if is_positive and pred in action.add_list:
                    relevant_actions.append(action)
                    break
                elif not is_positive and pred in action.delete_list:
                    relevant_actions.append(action)
                    break
        
        results = []
        # Step 2: Try all possible subsets of relevant actions
        for r in range(1, len(relevant_actions) + 1):
            for action_set in combinations(relevant_actions, r):
                # Step 3: Check if this action set covers all goals
                covered_goals = set()
                for action in action_set:
                    # Add all effects of actions
                    for pred in action.add_list:
                        covered_goals.add((pred, True))
                    for pred in action.delete_list:
                        covered_goals.add((pred, False))
                
                # Skip this action set if it doesn't cover all goals
                if not set(goals).issubset(covered_goals):
                    continue
                
               

                # Step 4: Check if any two actions in the set are mutex
                ...
                
                # Step 5: If mutex-free, add to results
                ...

               
                    
        return results

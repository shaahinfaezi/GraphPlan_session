from Model.GraphAction import StateLevel, ActionLevel, PersistenceAction, Action
from Problems.Problem import Problem
from PlanningGraph.GraphPlot import GraphPlot
from itertools import combinations

class PlanningGraph:
    """
    GraphPlan's planning graph: alternating levels of states and actions.
    Graph represents what's achievable at each time step and what's impossible (mutexes).
    """
    
    def __init__(self, problem: Problem):
        """
        Initialize the planning graph with the initial state.
        
        Steps:
        1. Collect all possible predicates from domain actions
        2. Create initial state level (S0) with positive/negative literals
        3. Convert domain actions to graph actions
        4. Convert goal predicates to goal literals
        """
        self.problem = problem
        self.graph_plot = GraphPlot()
        
        # Step 1: Collect all predicates that appear in any action
        all_predicates = set()
        for act in problem.domain.actions:
            all_predicates.update(act.positive_preconditions)
            all_predicates.update(act.negative_preconditions)
            all_predicates.update(act.add_list)
            all_predicates.update(act.delete_list)
        
        # Step 2: Create initial state level with Closed World Assumption
        # (everything not mentioned is false)
        s0 = StateLevel()
        
        # Add predicates that are true in initial state
        for p in problem.initial_state.literals:
            s0.positive_literals.add(p)
        
        # Add predicates that are false (implicitly)
        for p in all_predicates:
            if p not in problem.initial_state.literals:
                s0.negative_literals.add(p)
        
        # Step 3: Convert domain actions (for backward planner) to graph actions
        self.all_actions = set()
        for act in problem.domain.actions:
            self.all_actions.add(Action(
                act.action_name,
                act.positive_preconditions,
                act.negative_preconditions,
                act.add_list,
                act.delete_list
            ))
        
        # Step 4: Convert goal state to (predicate, is_positive) tuples
        self.goal = set()
        for p in problem.goal_state.literals:
            self.goal.add((p, True))
        
        # Initialize graph with just the initial state
        self.levels = []
        self.levels.append(s0)
        self.graph_plot.print_level(0, self.levels)

    def expand_graph(self):
        """
        Expand the planning graph by one iteration.
        
        Steps:
        1. Find actions applicable in current state
        2. Add persistence actions (no-ops) for each literal
        3. Calculate action mutexes
        4. Create next state from action effects
        5. Calculate literal mutexes
        """
        last_state = self.levels[-1]
        action_layer = ActionLevel()
        
        # Step 1: Find all applicable actions (preconditions satisfied)
        for action in self.all_actions:
            # Check if positive preconditions are in state
            pos_satisfied = action.positive_preconditions.issubset(last_state.positive_literals)
            # Check if negative preconditions are in state
            neg_satisfied = action.negative_preconditions.issubset(last_state.negative_literals)
            if pos_satisfied and neg_satisfied:
                action_layer.actions.add(action)
        
        # Step 2: Add persistence actions (no-ops) for each positive literal
        for p in last_state.positive_literals:
            persist = PersistenceAction(
                p,
                is_positive=True,
                positive_preconditions={p},
                negative_preconditions=set(),
                add_list={p},
                delete_list=set()
            )
            action_layer.actions.add(persist)
        
        # Step 2b: Add persistence actions for each negative literal
        for p in last_state.negative_literals:
            persist = PersistenceAction(
                p,
                is_positive=False,
                positive_preconditions=set(),
                negative_preconditions={p},
                add_list=set(),
                delete_list={p}
            )
            action_layer.actions.add(persist)
        
        # Step 3: Calculate which actions are mutually exclusive
        self._calculate_action_mutexes(action_layer, last_state)
        
        self.levels.append(action_layer)
        self.graph_plot.print_level(len(self.levels)-1, self.levels)
        
        # Step 4: Create next state level from action effects
        next_state = StateLevel()
        
        # Add all positive effects (add_list) from actions
        for action in action_layer.actions:
            for p in action.add_list:
                next_state.positive_literals.add(p)
            # Add all negative effects (delete_list) 
            for p in action.delete_list:
                next_state.negative_literals.add(p)
        
        # Step 5: Calculate which literals are mutually exclusive
        self._calculate_literal_mutexes(next_state, action_layer)
        
        self.levels.append(next_state)
        self.graph_plot.print_level(len(self.levels)-1, self.levels)
        
        # Display the updated graph
        self.graph_plot.plot_graph(self.levels)

    def _calculate_action_mutexes(self, action_layer, last_state):
        """
        Two actions are mutex (mutually exclusive) if:
        1. Inconsistent Effects: One adds what the other deletes
        2. Interference: One deletes a precondition of the other
        3. Competing Needs: Their preconditions are mutex
        """
        actions = list(action_layer.actions)
        for i in range(len(actions)):
            for j in range(i + 1, len(actions)):
                a1 = actions[i]
                a2 = actions[j]
                
                mutex = False
                



                # Reason 1: Inconsistent Effects
                ...
                
                # Reason 2: Interference
                ...
                
                # Reason 3: Competing Needs
                if not mutex:
                    # Convert preconditions to (predicate, bool) tuples
                    pre1 = set()
                    for p in a1.positive_preconditions: 
                        pre1.add((p, True))
                    for p in a1.negative_preconditions: 
                        pre1.add((p, False))
                    
                    pre2 = set()
                    for p in a2.positive_preconditions: 
                        pre2.add((p, True))
                    for p in a2.negative_preconditions: 
                        pre2.add((p, False))
                    


                    # Check for competing needs
                    ...

                
                # Store the mutex relation
                if mutex:
                    action_layer.action_mutex.add(frozenset({a1, a2}))

    def _calculate_literal_mutexes(self, next_state, action_layer):
        """
        Two literals are mutex if:
        1. Negation: They are P and ~P
        2. Inconsistent Support: All action pairs that could produce them are mutex
        """
        def get_producers(pred, is_pos, layer):
            """Find all actions that produce this literal."""
            producers = []
            for a in layer.actions:
                if is_pos:
                    if pred in a.add_list: 
                        producers.append(a)
                else:
                    if pred in a.delete_list: 
                        producers.append(a)
            return producers

        # Create list of all literals
        literals = []
        for p in next_state.positive_literals: 
            literals.append((p, True))
        for p in next_state.negative_literals: 
            literals.append((p, False))
        
        # Check all pairs of literals
        for i in range(len(literals)):
            for j in range(i + 1, len(literals)):
                l1 = literals[i]
                l2 = literals[j]
                
                pred1, val1 = l1
                pred2, val2 = l2
                
                mutex = False
                
                # Get actions that produce each literal
                producers1 = get_producers(pred1, val1, action_layer)
                producers2 = get_producers(pred2, val2, action_layer)
                
                # Reason 1: Negation
                # Same predicate with opposite truth values
                if pred1 == pred2 and val1 != val2:
                    mutex = True
                
                # Reason 2: Inconsistent Support
                # All ways to produce l1 conflict with all ways to produce l2
                elif producers1 and producers2:
                    all_pairs_mutex = True
                    for a1 in producers1:
                        for a2 in producers2:
                            # Same action can produce both
                            if a1 == a2:
                                all_pairs_mutex = False
                                break
                            # Actions are not mutex (can be done together)
                            if frozenset({a1, a2}) not in action_layer.action_mutex:
                                all_pairs_mutex = False
                                break
                        if not all_pairs_mutex: 
                            break
                    
                    if all_pairs_mutex:
                        mutex = True
                
                # Store the mutex relation
                if mutex:
                    next_state.literal_mutex.add(frozenset({l1, l2}))

    def check_goal_achievable(self, goal_literals):
        """
        Check if all goals can be achieved in the current state level.
        Goals are achievable if:
        1. All goal literals are present in the current state
        2. No pair of goal literals has a mutex relation
        """
        last_state = self.levels[-1]
        if not isinstance(last_state, StateLevel):
            return False
        
        # Check 1: All goals are present
        for pred, val in goal_literals:
            if val:
                # Positive literal must be in positive_literals
                if pred not in last_state.positive_literals:
                    return False
            else:
                # Negative literal must be in negative_literals
                if pred not in last_state.negative_literals:
                    return False
        
        # Check 2: No mutex between goals
        goals = list(goal_literals)
        for i in range(len(goals)):
            for j in range(i + 1, len(goals)):
                g1 = goals[i]
                g2 = goals[j]
                
                pred1, val1 = g1
                pred2, val2 = g2
                
                # Same predicate, opposite values = always mutex
                if pred1 == pred2 and val1 != val2:
                    return False
                # Check mutex set
                if frozenset({g1, g2}) in last_state.literal_mutex:
                    return False
        
        return True

    def has_levelled_off(self):
        """
        Check if the graph has reached a fixed point.
        Graph levels off when two consecutive state levels are identical.
        This means no new literals can be added, so no solution is possible.
        """
        if len(self.levels) < 3:
            return False
        
        # Compare last state level with state level before the action layer
        last_level = self.levels[-1]
        prev_level = self.levels[-3]
        
        if not isinstance(last_level, StateLevel) or not isinstance(prev_level, StateLevel):
            return False
        
        # Check if positive literals haven't changed
        if last_level.positive_literals != prev_level.positive_literals:
            return False
        # Check if negative literals haven't changed
        if last_level.negative_literals != prev_level.negative_literals:
            return False
        # Check if mutexes haven't changed
        if last_level.literal_mutex != prev_level.literal_mutex:
            return False
        
        # All identical = graph leveled off
        return True

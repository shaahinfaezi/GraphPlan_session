from Model.Predicate import Predicate
from Model.Action import Action

class StateLevel:
    """
    Represents a state level in the planning graph.
    Contains all propositions (literals) that are true at this time step.
    
    Attributes:
        positive_literals: Set of predicates that are TRUE (e.g., At(A,B))
        negative_literals: Set of predicates that are FALSE (e.g., At(A,C))
        literal_mutex: Set of mutex pairs between literals
    """
    def __init__(self):
        self.positive_literals = set()  # Propositions that are true
        self.negative_literals = set()  # Propositions that are false
        self.literal_mutex = set()      # Pairs of conflicting propositions

    @property
    def propositions(self):
        """Return all propositions (positive + negative literals)."""
        return self.positive_literals | self.negative_literals

    def __repr__(self):
        return f"StateLevel({len(self.propositions)} literals)"

class ActionLevel:
    """
    Represents an action level in the planning graph.
    Contains all actions that can be executed at this time step.
    
    Attributes:
        actions: Set of applicable actions
        action_mutex: Set of mutex pairs between actions
    """
    def __init__(self):
        self.actions = set()          # Actions that can be executed
        self.action_mutex = set()     # Pairs of conflicting actions

    def __repr__(self):
        return f"ActionLevel({len(self.actions)} actions)"

class PersistenceAction(Action):
    """
    A no-op action that maintains a literal unchanged.
    Represents that a fact can remain true (or false) without doing anything.
    
    For example: Persist(At(A,B)) means "A stays at B without moving"
    
    Attributes:
        proposition: The predicate being maintained
        is_positive: True if maintaining a positive fact, False for negative
    """
    def __init__(self, proposition: Predicate, is_positive: bool, positive_preconditions: set, negative_preconditions: set, add_list: set, delete_list: set):
        # Create a descriptive name for this persistence action
        if is_positive:
            name = f"Persist({proposition})"
        else:
            name = f"Persist(~{proposition})"
        # Call parent Action constructor
        super().__init__(name, positive_preconditions, negative_preconditions, add_list, delete_list)
        # Store the proposition this action maintains
        self.proposition = proposition
        self.is_positive = is_positive

    def __repr__(self):
        return self.name

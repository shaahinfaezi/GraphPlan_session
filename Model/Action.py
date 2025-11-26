from Model.Predicate import Predicate
from Model.State import State

class Action:
    """
    Represents an action in the planning domain.
    
    Attributes:
        name: Name of the action (e.g., "Move(A,B,C)")
        positive_preconditions: Set of predicates that must be true
        negative_preconditions: Set of predicates that must be false
        add_list: Set of predicates that become true after action
        delete_list: Set of predicates that become false after action
    """
    
    def __init__(
        self,
        name: str = None,
        positive_preconditions: set[Predicate] = None,
        negative_preconditions: set[Predicate] = None,
        add_list: set[Predicate] = None,
        delete_list: set[Predicate] = None,
        action_name: str = None,  # Backward compatibility
    ):
        self.name = action_name if action_name else name
        # Initialize empty sets if not provided
        self.positive_preconditions = positive_preconditions if positive_preconditions else set()
        self.negative_preconditions = negative_preconditions if negative_preconditions else set()
        self.add_list = add_list if add_list else set()
        self.delete_list = delete_list if delete_list else set()

    def is_applicable(self, state) -> bool:
        """
        Check if action can be executed in the given state.
        Action is applicable if:
        - All positive preconditions are in the state
        - All negative preconditions are NOT in the state (Closed World Assumption)
        """
        state_preds = state.literals
        # Check positive preconditions are satisfied
        pos_ok = self.positive_preconditions.issubset(state_preds)
        # Check negative preconditions are not in state
        neg_ok = self.negative_preconditions.isdisjoint(state_preds)
        return pos_ok and neg_ok

    def progress(self, state):
        """
        Forward step: Apply action to state to get new state.
        New state = old state - delete_list + add_list
        """
        new_preds = state.literals.copy()
        new_preds -= self.delete_list  # Remove deleted predicates
        new_preds |= self.add_list      # Add new predicates
        return State(self.name, list(new_preds))

    def is_relevant(self, state: State) -> bool:
        """
        Check if action is relevant for backward search.
        Action is relevant if its effects help achieve the goal.
        """
        # Must add at least one goal predicate (or have no effects)
        adds_goal = (not self.add_list.isdisjoint(state.literals)) or (len(self.add_list) == 0)
        # Must not require something we're deleting
        no_conflict = ((self.negative_preconditions.copy() - self.add_list).isdisjoint(state.literals))
        return adds_goal and no_conflict

    def regress(self, state: State) -> State:
        """
        Backward step: Get preconditions needed before this action.
        Preconditions = (state - add_list) + positive_preconditions
        """
        regressed = state.literals.copy()
        regressed -= self.add_list              # Remove what this action adds
        regressed |= self.positive_preconditions  # Add what it requires
        return State(action_name="", literals=list(regressed))

    def __repr__(self):
        """String representation of action (just its name)."""
        return self.name

    def __eq__(self, other):
        """Two actions are equal if they have the same name."""
        if not isinstance(other, Action):
            return False
        return self.name == other.name

    def __hash__(self):
        """Hash based on action name (allows actions in sets/dicts)."""
        return hash(self.name)

    @property
    def action_name(self):
        """Property for backward compatibility."""
        return self.name

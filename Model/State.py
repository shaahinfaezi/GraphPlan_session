from Model.Predicate import Predicate


class State:
    def __init__(
        self,
        action_name: str,
        literals: list[Predicate],
    ):
        # Initialize a State object
        self.action_name = action_name  # Set the name of the action
        for p in literals:
            assert isinstance(
                p, Predicate
            ), f"positive literals should be type of Predicate not {p.__class__} "
        self.literals = set(
            literals
        )  # Convert literals to a set
        self.parent = None

    def goal_test(self, goal):
        is_all_positive = goal.literals.issubset(self.literals)
        return is_all_positive

    def initial_test(self, initial):
        # this part has been changed because it didn't made sense having it as is current state literals 
        # being subset of initial state literals, all initial and current state literals must be equal
        is_all_positive = (self.literals == initial.literals)
        return is_all_positive

    def build_solution(self) -> list:
        result = []
        state = self
        while state.parent:
            result.append(state.action_name)
            state = state.parent
        result.reverse()
        return result

    def __eq__(self, other) -> bool:
        # Check if two State entities are equal
        return self.literals == other.literals

    def __lt__(self, other):
        return self.action_name < other.action_name

    def __hash__(self) -> int:
        # Compute the hash value of the State object
        result = 0
        PRIME = 1073741789  # A prime number for hashing

        # Hash each positive literal in the set of positive literals
        for positive_literal in self.literals:
            result = (result + (positive_literal.__hash__() % PRIME)) % PRIME

        return result

    def __str__(self) -> str:
        return (
            "Action: "
            + self.action_name
            + "\n"
            + "Positive Literals: "
            + ", ".join(
                [str(positive_literal) for positive_literal in self.literals]
            )
            + "\n"
        )

    def __repr__(self) -> str:
        return str(self)

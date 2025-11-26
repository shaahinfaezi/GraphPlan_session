from Model.State import State
from Problems.Problem import Problem
from Model.Predicate import Predicate

class CakeProblem(Problem):
    def __init__(self, domain):
        super().__init__(domain)
        cake = domain.entities[0]
        self.initial_state = State(
            action_name="Init",
            literals=[Predicate("Have", [cake])]
        )
        self.goal_state = State(    
            action_name="Goal",
            literals=[
                Predicate("Have", [cake]),
                Predicate("Eaten", [cake])
            ]
        )
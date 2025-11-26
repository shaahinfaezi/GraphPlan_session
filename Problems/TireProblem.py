from Domains.Domain import Domain
from Model.Predicate import Predicate
from Model.State import State
from Problems.Problem import Problem


class Tire(Problem):
    def __init__(self, domain: Domain):
        super().__init__(domain)

        at_flat_axle = Predicate("At", [domain.flat, domain.axle])

        at_spare_trunk = Predicate("At", [domain.spare, domain.trunk])

        self.initial_state = State(
            "",
            [at_flat_axle, at_spare_trunk],
        )

        at_spare_axel = Predicate("At", [domain.spare, domain.axle])

        at_flat_ground = Predicate("At", [domain.flat, domain.ground])

        self.goal_state = State("", [at_spare_axel,at_flat_ground])

from Domains.Domain import Domain
from Model.Entity import Entity
from Model.Predicate import Predicate
from Model.State import State
from Problems.Problem import Problem


class SatelliteProblem(Problem):
    def __init__(self, domain: Domain):
        super().__init__(domain)
        rocket = Entity("Rocket", "Rocket")
        satellite1 = Entity("Satellite1", "Satellite")
        satellite2 = Entity("Satellite2", "Satellite")
        launch_pad = Entity("LaunchPad", "LaunchPad")
        orbit = Entity("Orbit", "Orbit")

        rocket_on_pad = Predicate("RocketOn", [rocket, launch_pad])
        satellite1_ready = Predicate("Satellite1Ready", [satellite1])
        satellite2_ready = Predicate("Satellite2Ready", [satellite2])
        orbit_defined = Predicate("OrbitDefined", [orbit])

        self.initial_state = State(
            "",
            [
                rocket_on_pad,
                satellite1_ready,
                satellite2_ready,
                orbit_defined
            ]
        )

        satellite1_in_orbit = Predicate("Satellite1InOrbit", [satellite1, orbit])
        satellite2_in_orbit = Predicate("Satellite2InOrbit", [satellite2, orbit])

        self.goal_state = State(
            "",
            [
                satellite1_in_orbit,
                satellite2_in_orbit
            ]
        )
from Domains.Domain import Domain
from Model.Action import Action
from Model.Entity import Entity
from Model.Predicate import Predicate


class SatelliteDomain(Domain):
    def __init__(self):
        super().__init__("Satellite Domain")
        self.rocket = Entity("Rocket", "Rocket")
        self.satellite1 = Entity("Satellite1", "Satellite")
        self.satellite2 = Entity("Satellite2", "Satellite")
        self.launch_pad = Entity("LaunchPad", "LaunchPad")
        self.orbit = Entity("Orbit", "Orbit")
        self.entities = [self.rocket, self.satellite1, self.satellite2, self.launch_pad, self.orbit]

    

    @Domain.schema
    def load_satellite2(self, rocket, satellite2, launch_pad):
        if rocket.type != "Rocket" or satellite2.type != "Satellite" or launch_pad.type != "LaunchPad":
            return None
        action_name = f"LoadSatellite2({rocket.name},{satellite2.name},{launch_pad.name})"
        rocket_on_pad = Predicate("RocketOn", [rocket, launch_pad])
        satellite2_ready = Predicate("Satellite2Ready", [satellite2])
        satellite2_in_rocket = Predicate("Satellite2In", [satellite2, rocket])

        return Action(
            action_name,
            {rocket_on_pad, satellite2_ready},
            set(),
            {satellite2_in_rocket},
            {satellite2_ready}
        )
    
    @Domain.schema
    def load_satellite1(self, rocket, satellite1, launch_pad):
        if rocket.type != "Rocket" or satellite1.type != "Satellite" or launch_pad.type != "LaunchPad":
            return None
        action_name = f"LoadSatellite1({rocket.name},{satellite1.name},{launch_pad.name})"
        rocket_on_pad = Predicate("RocketOn", [rocket, launch_pad])
        satellite1_ready = Predicate("Satellite1Ready", [satellite1])
        satellite1_in_rocket = Predicate("Satellite1In", [satellite1, rocket])

        return Action(
            action_name,
            {rocket_on_pad, satellite1_ready},
            set(),
            {satellite1_in_rocket},
            {satellite1_ready}
        )

    @Domain.schema
    def fuel_rocket(self, rocket, launch_pad):
        if rocket.type != "Rocket" or launch_pad.type != "LaunchPad":
            return None
        action_name = f"FuelRocket({rocket.name},{launch_pad.name})"
        rocket_on_pad = Predicate("RocketOn", [rocket, launch_pad])
        rocket_fueled = Predicate("RocketFueled", [rocket])

        return Action(
            action_name,
            {rocket_on_pad},
            set(),
            {rocket_fueled},
            set()
        )

    @Domain.schema
    def launch_rocket(self, rocket, satellite1, satellite2, launch_pad, orbit):
        if (rocket.type != "Rocket" or satellite1.type != "Satellite" or 
            satellite2.type != "Satellite" or launch_pad.type != "LaunchPad" or orbit.type != "Orbit"):
            return None
        action_name = f"LaunchRocket({rocket.name},{satellite1.name},{satellite2.name},{launch_pad.name},{orbit.name})"
        rocket_on_pad = Predicate("RocketOn", [rocket, launch_pad])
        rocket_fueled = Predicate("RocketFueled", [rocket])
        satellite1_in_rocket = Predicate("Satellite1In", [satellite1, rocket])
        satellite2_in_rocket = Predicate("Satellite2In", [satellite2, rocket])
        orbit_defined = Predicate("OrbitDefined", [orbit])
        rocket_in_orbit = Predicate("RocketIn", [rocket, orbit])

        return Action(
            action_name,
            {rocket_on_pad, rocket_fueled, satellite1_in_rocket, satellite2_in_rocket, orbit_defined},
            set(),
            {rocket_in_orbit},
            {rocket_on_pad}
        )

    @Domain.schema
    def deploy_satellite1(self, rocket, satellite1, orbit):
        if rocket.type != "Rocket" or satellite1.type != "Satellite" or orbit.type != "Orbit":
            return None
        action_name = f"DeploySatellite1({rocket.name},{satellite1.name},{orbit.name})"
        rocket_in_orbit = Predicate("RocketIn", [rocket, orbit])
        satellite1_in_rocket = Predicate("Satellite1In", [satellite1, rocket])
        satellite1_in_orbit = Predicate("Satellite1InOrbit", [satellite1, orbit])

        return Action(
            action_name,
            {rocket_in_orbit, satellite1_in_rocket},
            set(),
            {satellite1_in_orbit},
            {satellite1_in_rocket}
        )

    @Domain.schema
    def deploy_satellite2(self, rocket, satellite2, orbit):
        if rocket.type != "Rocket" or satellite2.type != "Satellite" or orbit.type != "Orbit":
            return None
        action_name = f"DeploySatellite2({rocket.name},{satellite2.name},{orbit.name})"
        rocket_in_orbit = Predicate("RocketIn", [rocket, orbit])
        satellite2_in_rocket = Predicate("Satellite2In", [satellite2, rocket])
        satellite2_in_orbit = Predicate("Satellite2InOrbit", [satellite2, orbit])

        return Action(
            action_name,
            {rocket_in_orbit, satellite2_in_rocket},
            set(),
            {satellite2_in_orbit},
            {satellite2_in_rocket}
        )
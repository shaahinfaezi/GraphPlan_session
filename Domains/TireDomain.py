from Domains.Domain import Domain
from Model.Action import Action
from Model.Entity import Entity
from Model.Predicate import Predicate


class TireDomain(Domain):
    def __init__(self):
        super().__init__("Tire Domain")
        self.flat = Entity("Flat", "Tire")
        self.spare = Entity("Spare", "Tire")
        self.axle = Entity("Axle", "Location")
        self.trunk = Entity("Trunk", "Location")
        self.ground = Entity("Ground", "Ground")
        self.entities.append(self.flat)
        self.entities.append(self.axle)
        self.entities.append(self.spare)
        self.entities.append(self.ground)
        self.entities.append(self.trunk)

    @Domain.schema
    def remove_action(self, obj, loc):
        if not (obj.type == "Tire" and loc.type == "Location"):
            return None
        at_loc = Predicate("At", [obj, loc])
        at_action_name = f"Remove({obj.name},{loc.name})"
        at_ground = Predicate("At", [obj, self.ground])

        return Action(
            at_action_name, 
            {at_loc},
            set(),
            {at_ground},
            {at_loc},
        )

    @Domain.schema
    def PutOn_action(self, t):
        if t.type != "Tire":
            return None
        at_t = Predicate("At", [t, self.ground])
        at_axle = Predicate("At", [self.flat, self.axle])
        at_spare = Predicate("At", [self.spare, self.axle])
        at_action_name = f"PutOn({t.name},{self.axle.name})"

        at_t_axle = Predicate("At", [t, self.axle])

        return Action(
            at_action_name,
            {at_t},
            {at_axle, at_spare},
            {at_t_axle},
            {at_t},
        )

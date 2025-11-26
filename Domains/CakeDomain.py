from Model.Entity import Entity
from Model.Predicate import Predicate
from Model.Action import Action
from Domains.Domain import Domain

class CakeDomain(Domain):
    def __init__(self):
        super().__init__("CakeDomain")
        self.entities = [
            Entity(name="Cake", type="object")
        ]

    @Domain.schema
    def eat_cake(self, cake):
        return Action(
            action_name="EatCake",
            positive_preconditions={Predicate("Have", [cake])},
            negative_preconditions=set(),
            add_list={Predicate("Eaten", [cake])},
            delete_list={Predicate("Have", [cake])}
        )
    
    @Domain.schema
    def bake_cake(self, cake):
        return Action(
            action_name="BakeCake",
            positive_preconditions={},
            negative_preconditions={Predicate("Have", [cake])},
            add_list={Predicate("Have", [cake])},
            delete_list={}
        )
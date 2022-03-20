import secrets
from pprint import pprint
from collections import defaultdict
from dataclasses import dataclass, field, fields
from typing import Optional


def new_token():
    token = secrets.token_hex(16)
    while token in System.Entities:
        token = secrets.token_hex(16)
    return token


class System:
    Entities = {}  # key-values pairs of Entity 'id' and instance
    Components = defaultdict(list)


@dataclass
class Component:
    _id: Optional[str] = field(init=False)  # id of instantiating entity

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        print(f"ids: {self._id} vs. {value}")
        #assert self._id == None
        self._id = value
        System.Components[self.__class__.__name__].append(self)
        
    def __post_init__(self):
        self._id = None


@dataclass
class Entity:
    id: str = field(default_factory=new_token)

    def __post_init__(self):
        print(f"id: {self.id}")
        for field_ in fields(self):
            print(field_)
            if Component in field_.type.__mro__:
                component = getattr(self, field_.name)
                component.id = self.id
        System.Entities.update({self.id: self})


@dataclass
class ChildComp(Component):
    color: str = "blue"


@dataclass
class ChildEnt(Entity):
    one: ChildComp = field(default_factory=ChildComp)
    two: ChildComp = field(default_factory=ChildComp)


ent1 = ChildEnt(id="1",one=ChildComp(color='red'))
ent2 = ChildEnt(id="2",two=ChildComp(color='green'))
# Write a test which ensures for a large set that all components for a given entity have the correct id

pprint({'Entities': System.Entities, 'Components': System.Components})


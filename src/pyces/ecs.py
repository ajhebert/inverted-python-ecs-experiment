from abc import ABC, abstractmethod
import secrets
from pprint import pprint
from collections import defaultdict
from dataclasses import dataclass, field, fields
from typing import Optional
from collections import defaultdict
from functools import partial

class MetaComponent(type):
    registry = {}

    # def __class_registry__(cls) -> dict: # type: ignore
    #     return MetaComponent.registry[cls.__name__]
        
    def __new__(cls, name, bases, class_dict):
        MetaComponent.registry[name] = []
        Class = super().__new__(cls, name, bases, class_dict)
        Class.__init_subclass__ = partial(cls.__init_subclass__, name)
        return Class

component_registry = {}

class _Component:
    
    def __set_name__(self, owner, name):
        print(owner)
        self.name = name
        
    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value) -> None:
        obj.__dict__[self.name] = value

class Component(metaclass=MetaComponent):
    """
    Components are the building blocks of compositional objects,
    a.k.a., Entities. Components are comprised of data fields,
    and lack methods of any kind except, perhaps, factories.

    All Components (and subclasses) _must_ be dataclasses.
    """
    
    def __init_subclass__(cls, name):
        MetaComponent.registry[name] += [cls]
        
    # @classmethod
    # def __init__(cls, self):
    #     self.registry[cls.__name__] += [self]

    _registry = defaultdict(list)
    """Only meant to be accessed outside of class by Systems"""
    _entity: Optional[str] = field(
        default=None, init=False
    )  # id of instantiating entity

    @classmethod
    @property
    def all(cls) -> dict:
        return Component._registry

    @classmethod
    @property
    def registry(cls) -> any:
        return Component._registry[cls.__name__]

    @property
    def entity(self):
        """
        The entity which is composed with this component.

        a.k.a., the 'parent' entity
        """
        return self._entity

    @entity.setter
    def entity(self, value):
        assert self._entity == None, f"Changing parent entity not allowed"
        self._entity = value
        if value not in self.registry:
            self.registry.append(value)


@dataclass
class Entity:
    """
    Entities bind Components together into cohesive ideas relevant
    to Systems.

    All Entities (and subclasses) _must_ be dataclasses.
    """

    def new_token():
        token = secrets.token_hex(16)
        while token in Entity._registry:
            token = secrets.token_hex(16)
        return token

    _registry = defaultdict(None)
    id: str = field(default_factory=new_token)

    @classmethod
    @property
    def registry(cls) -> any:
        """
        Entities are registered by their unique token
        so Systems can quickly look up an Entity from
        a Component's entity (:str).

        Returns:
            dict of id:Entity (key:value) pairs
        """
        return Entity._registry

    def __post_init__(self, *args, **kwargs):
        for field_ in fields(self):
            if Component in field_.type.__mro__:
                component = getattr(self, field_.name)
                component.entity = self.id
        self.registry[self.id] = self
        self.__post_reg__(*args, **kwargs)

    def __post_reg__(self):
        """
        Post-registration, any class which inherits from Entity
        and needs to 'initialize' its attributes should write
        this function.

        Allegory:
        __init__        => class
        __post_init__   => dataclass
        __post_reg__    => Entity

        """
        ...


class System(ABC):
    @property
    @abstractmethod
    def components() -> list[Component]:
        """
        The 'list' of components, a System may operate on only
        those entities which possess all listed Components.
        """
        ...

    @classmethod
    @property
    def entities(cls) -> list[str]:
        """All Entities composed with all components attributed to this System.

        Returns:
            list[str]: list of Entities possessing all components required
                        by this System
        """
        assert len(cls.components) > 0
        index = cls.components[0].__name__
        if len(cls.components) == 1:
            return Component.all[index]
        else:
            result = Component.all[index]
            for component in cls.components:
                index = component.__name__
                result.append([x for x in result if x in Component.all[index]])
            return result

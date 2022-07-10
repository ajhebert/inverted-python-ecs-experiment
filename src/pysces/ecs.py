# MIT License

# Copyright (c) 2022 Andrew Hebert Jr.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from abc import ABC, abstractmethod
import secrets
from pprint import pprint
from collections import defaultdict
from dataclasses import dataclass, field, fields
from typing import Optional


@dataclass
class Component:
    """
    Components are the building blocks of compositional objects,
    a.k.a., Entities. Components are comprised of data fields,
    and lack methods of any kind except, perhaps, factories.

    All Components (and subclasses) _must_ be dataclasses.
    """

    _registry = defaultdict(
        list
    )  # Only meant to be accessed outside of class by Systems
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

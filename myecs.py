import secrets
from collections import defaultdict

_System = defaultdict(list)

class Component:
    _entity = None
    
    @property
    def entity(self):
        return self._entity

    @property.setter
    def entity(self, value):
        assert self._entity == None
        self._entity = value
        
        # Register the Component in the System
        _System[self.__class__.__name__].append(self)
        

class Entity:
    # I want to define entities such that I can use a decorator to say "this is a component", 
    # and be able to refer to an entity's components like a traditional object,
    # and also add them to lists for bulk processing.
    _components: dict = {}
    
    def component(self, obj: Component):
        self._components.append(obj)
    
    def __init__(self, *objs: Component):
        pass
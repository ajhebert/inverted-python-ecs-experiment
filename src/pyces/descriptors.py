import logging, textwrap
from typing import  ClassVar, TypeVar
from pprint import pformat

logger = logging.getLogger(__name__)

def format_log(obj):
    if len(obj) == 0:
        return ""
    return "\n"+textwrap.indent(pformat(obj, indent=4, compact=False), " "*4)+"\n"

__components_set_string__ = "__components_set__"
__components_string__ = "__components__"

InterfaceType = TypeVar('InterfaceType')

class Component:
    logger = logging.getLogger(__name__+'.Component')
    registry: ClassVar[dict[InterfaceType, list]] = {}
    interface: InterfaceType
    
    def __set_name__(self, owner, name):
        self.logger.debug(f"__set_name__({format_log(locals())})")
        self.name = name
        try:
            self.interface = owner.__annotations__[name]
        except KeyError:
            raise RuntimeError("Cannot assign Component to untyped attribute")
        Component.registry[self.interface] = []
            
        if __components_set_string__ not in owner.__dict__:
            setattr(owner, __components_set_string__, set([self.name]))
            setattr(owner, __components_string__, property(fget=lambda self: list(getattr(self,__components_set_string__))))
        else:
            owner.__dict__[__components_set_string__].add(self.name)
        
    def __get__(self, obj, type_=None) -> InterfaceType:
        self.logger.debug(f"__get__({format_log(locals())})")
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value: InterfaceType) -> None:
        self.logger.debug(f"__set__({format_log(locals())})")
        if self.name not in obj.__dict__:
            Component.registry[self.interface] += [obj]
        obj.__dict__[self.name] = self.interface(value)

    def __del__(self, obj, *_) -> None: # TODO Write tests for this.
        self.logger.debug(f"__del__({format_log(locals())})")
        delx = Component.registry[self.interface].index(self)
        del Component.registry[self.interface][delx]
        del obj.__dict__[self.name]

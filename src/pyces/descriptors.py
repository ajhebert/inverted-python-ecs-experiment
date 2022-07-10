import logging, colorama
from typing import Optional
from pprint import pformat
from pydantic import BaseModel

colorama.init()

BLUE = colorama.Fore.BLUE
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

logger = logging.getLogger(__name__)

def _format(obj):
    return YELLOW + pformat(obj) + RESET


__components_set_string__ = "__components_set__"
__components_string__ = "__components__"


class _Interfaced(type):
    def __new__(cls, name, bases, class_dict):
        print(class_dict)
        super().__new__(cls, name, bases, class_dict)
        ...

class Component(metaclass=_Interfaced):
    registry = {}
    _model: Optional[BaseModel] = None # should move checking to metaclass
    
    def __init__(self):
        try:
            assert BaseModel in self._model.__mro__ if self._model != None else True
        except AssertionError:
            raise TypeError(f"{repr(self._model)} must be an instance of {repr(BaseModel.__qualname__)}")
    
    def __set_name__(self, owner, name):
        logger.info(f"{BLUE}__set_name__{RESET}(self=%s, owner=%s, name=%s) ...", _format(self), _format(owner), _format(name))
        self.name = name
        # Track all components in the owner.
        if __components_set_string__ not in owner.__dict__:
            setattr(owner, __components_set_string__, set([name]))
            setattr(owner, __components_string__, property(fget=lambda self: list(getattr(self,__components_set_string__))))
        else:
            is_duplicate = ( name in owner.__dict__.get(__components_set_string__) )
            assert not is_duplicate, f"duplicate Component( name={repr(name)} ) initialized in {owner.__name__}"
            owner.__dict__[__components_set_string__].add(name)
            #   I can't think of a reason components should be initialized more than once for a given name,
            #   so we'll catch it with an assertion. To ignore, catch it with a try-except block.
            
        if self.name not in self.registry:
            self.registry[self.name] = []
        
    def __get__(self, obj, type_=None) -> object:
        logger.info(f"{BLUE}__get__{RESET}(self=%s, obj=%s, type=%s) ...", _format(self), _format(obj), _format(type_))
        return obj.__dict__.get(self.name)
    
    def __set__(self, obj, value) -> None:
        logger.info(f"{BLUE}__set__{RESET}(self=%s, obj=%s, value=%s) ...", _format(self), _format(obj), _format(value))
        if self.name not in obj.__dict__:
            self.registry[self.name] += [obj]
        obj.__dict__[self.name] = value
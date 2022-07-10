import logging, colorama
from pprint import pformat

colorama.init()

BLUE = colorama.Fore.BLUE
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

logger = logging.getLogger(__name__)

def _format(obj):
    return YELLOW + pformat(obj) + RESET

def test_descriptor_nonesense():
    
    class Component:
        registry = {}
        
        def __set_name__(self, owner, name):
            logger.info(f"{BLUE}__set_name__{RESET}(self=%s, owner=%s, name=%s) ...", _format(self), _format(owner), _format(name))
            self.name = name
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
    
    class Something:
        foo = Component()
        boo = Component()
        
        def __init__(self):
            self.foo = 2
        
    something = Something()
    something_else = Something()
    print(something.foo)
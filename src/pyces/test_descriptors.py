import logging, colorama, pytest
from .descriptors import Component
from pydantic import BaseModel

colorama.init()

BLUE = colorama.Fore.BLUE
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

logger = logging.getLogger(__name__)


def test_descriptor_nonesense():
    
    class Something:
        foo: int = Component()
        boo = Component()
        
        def __init__(self):
            self.foo = 2
        
    something = Something()
    something_else = Something()
    print(something.foo)
    
def test_BaseModel_interface():
    """Checks """ 
    class Model(BaseModel): ...
    
    class ModeledComponent(Component):
        interface = Model
        
    class Something:
        foo: int = ModeledComponent()
        
    assert Something()
    
def test_BaseModel_type_error():
    
    with pytest.raises(TypeError):
        
        class BadComponent(Component):
            interface = int
        
        class Something:
            foo: int = BadComponent()
            
        _ = Something()
        
    
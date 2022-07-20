import logging
from .descriptors import *


logger = logging.getLogger(__name__)


def test_descriptor_nonesense():
    logger.info(f"TEST - test_descriptor_nonesense({format_log(locals())})")
    class Something:
        foo: int = Component()
        boo: str = Component()
        
        def __init__(self):
            self.foo = 2
            self.boo = 1.00
        
    something = Something()
    something_else = Something()
    print(something.foo)
    
def test_tuple_interface():
    logger.info(f"TEST - test_tuple_interface({format_log(locals())})")
        
    class MyEntity:
        xy_component: tuple[int, int] = Component

        def __init__(self, x: int, y: int):
            self.xy_component = (x, y)
        
    entity = MyEntity(x=1,y=1)
    assert entity.xy_component == (1, 1)
    
def test_init_subclass():
    logger.info(f"TEST - test_init_subclass({format_log(locals())})")
    
    # defining a SuperClass
    class SuperClass:
    
        # defining __init_subclass__ method
        def __init_subclass__(cls, **kwargs):
            cls.default_name ="Inherited Class"
    
    # defining a SubClass
    class SubClass(SuperClass):
    
        # an attribute of SubClass
        default_name ="SubClass" 
        print(default_name)
    
    subclass = SubClass()
    print(subclass.default_name)
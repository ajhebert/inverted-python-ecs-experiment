# from dataclasses import dataclass
# from functools import partial
# import black 
# from pprint import pformat
# from black.mode import Mode
# from .ecs import *


# # class ComponentSys(System):
# #     """
# #     This System tracks all entities which are composed
# #     with the base Component class.
# #     """

# #     components = [Component]


# # @dataclass
# # class MyEntity(Entity):
# #     one: Component = Component()
# #     two: Component = Component()
# #     three: Component = Component()


# # def test_component_system():
# #     myEntity = MyEntity(id="deadbeef")
# #     print(myEntity)
# #     assert len(ComponentSys.entities) == 1
# #     assert ComponentSys.entities[0] == "deadbeef"


# def test_meta_component():
#     class Comp0(Component): ...
#     class Comp1(Component): ...
#     class Comp2(Component): ...
#     assert MetaComponent.registry == {
#         "Component": [],
#         "Comp0": [],
#         "Comp1": [],
#         "Comp2": []
#     }
    

# def test_nonsense():
#     class Comp(Component): ...
        
#     class Entity:
#         def __init__(self):
#             Comp.__init__(self)
#             self.id = 0
            
#     entity = Entity()
#     pass

    
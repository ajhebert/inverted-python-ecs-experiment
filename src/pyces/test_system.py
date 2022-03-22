from dataclasses import dataclass
from .ecs import Entity, Component, System


class ComponentSys(System):
    """
    This System tracks all entities which are composed
    with the base Component class.
    """

    components = [Component]


@dataclass
class MyEntity(Entity):
    one: Component = Component()
    two: Component = Component()
    three: Component = Component()


def test_component_system():
    myEntity = MyEntity(id="deadbeef")
    print(myEntity)
    assert len(ComponentSys.entities) == 1
    assert ComponentSys.entities[0] == "deadbeef"

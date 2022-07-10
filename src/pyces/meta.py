import re
from collections import ChainMap


def _get_fields(obj) -> ChainMap:
    maps = []
    for cls in obj.__mro__:
        base_fields = {
            k: v
            for k, v in cls.__dict__.items()
            if not re.fullmatch(r"__[a-zA-Z_]\w+__", k)
        }
        maps.append(base_fields)
    return ChainMap(*maps)


class MetaClass(type):
    fields: ChainMap

    def __new__(cls, name, bases, fields):
        print("New Class: " + name)
        print(fields)
        obj = super().__new__(cls, name, bases, fields)
        fields_ = _get_fields(obj)
        print(dict(fields_))

        return obj


class SubClass(metaclass=MetaClass):
    foo = 1
    bar = 2


class SubSubClass(SubClass):
    foo = 3
    baz = 4


class SubSubSubClass(SubSubClass):
    baz = 5
    beef = 6

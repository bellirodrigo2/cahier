from abc import ABC, abstractmethod
from functools import partial
from typing import Generator

from pydantic import BaseModel, field_validator, Field,  AliasGenerator, ConfigDict
from pydantic.alias_generators import to_camel

##############################################################################
SPECIAL_CHARS = ['*', '?', ';', '{', '}', '[', ']', '|', '\\', '`', ''', ''', ':']
INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add('/')

def make_name(name) -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{name}{i}"
        i += 1


name_gen = make_name('newnode')


name_gen = make_name('newnode')


ObjConfig = partial(ConfigDict,
                alias_generator=AliasGenerator(
                    alias=to_camel,
                    validation_alias=to_camel,
                    serialization_alias=to_camel
                ),
                populate_by_name=True,
                use_enum_values=True,
                frozen=True,
                str_strip_whitespace=True,
                # extra='allow'
            )

NameField = partial(Field,
        description="Name Field Description",
        min_length=2,
        max_length=64,
        # default_factory=lambda: next(name_gen),
    ),

class BaseObj(BaseModel, ABC):
    
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        pass

    model_config = ObjConfig(extra='allow') #to allow derived class casting

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    id: str | None = NameField(default='_ID_')

class BaseRoot(BaseObj):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        return 'root'

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        return ['element', 'node']

    model_config = ObjConfig(extra='forbid')

class BaseElement(BaseObj):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        return 'element'

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra='forbid')
    
class BaseNode(BaseObj):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        return 'node'

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        return ['node', 'item']

    model_config = ObjConfig(extra='forbid')

    
class BaseItem(BaseObj):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        return 'item'

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        return ['item']

    model_config = ObjConfig(extra='forbid')
    
class Database(BaseRoot):
    pass
class User(BaseRoot):
    pass

class View(BaseElement):
    pass

class KeyValue(BaseElement):
    pass

class TemplateNode(BaseNode):
    pass

class Node(BaseNode):
    pass

class Item(BaseItem):
    pass

if __name__ == '__main__':
    print('OK')
#RECEBER DICT
#VALIDAR 

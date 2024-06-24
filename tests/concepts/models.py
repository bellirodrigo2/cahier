from functools import partial
from typing import Generator

from pydantic import BaseModel, field_validator, Field,  AliasGenerator, ConfigDict, ValidationError
from pydantic.alias_generators import to_camel

from cahier.schemas.makeenums import make_enum, EnumBase

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
        min_length=3,
        max_length=64,
        # default_factory=lambda: next(name_gen),
    )
IdField = partial(Field,
        description="Id Field Description",
        min_length=16,
        max_length=16,
        # default_factory=lambda: next(name_gen),
    )

class BaseObj(BaseModel):
    
    @classmethod
    def base_type(cls) -> str:
        return 'base'

    @classmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra='allow') #to allow derived class casting

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    id: str | None = IdField(default='_ID_')

class BaseRoot(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return 'root'

    @classmethod
    def children(cls) -> list[str]:
        return ['element', 'node']

    model_config = ObjConfig(extra='forbid')

class BaseElement(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return 'element'

    @classmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra='forbid')
    
class BaseNode(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return 'node'

    @classmethod
    def children(cls) -> list[str]:
        return ['node', 'item']

    model_config = ObjConfig(extra='forbid')

class BaseItem(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return 'item'

    @classmethod
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
    nodeattr1: str
    nodeattr2: str

class Item(BaseItem):
    itemattr: str

if __name__ == '__main__':
    print('Starting Tests')

    input = {
        'name': 'RBELLI',
        'id': '1234567890123456',
        'nodeattr1': 'field1node',
        'nodeattr2': 'field1node',
    }
    base = BaseObj(**input)
    node = Node(**base.model_dump())

    try:
        item = Item(**base.model_dump())
    except ValidationError as e:
        print('A Node cannot be casted to an Item')
        # print(e.json())
    try:
        input2 = dict(input)
        input2['extraattr'] = True
        base2 = BaseObj(**input2)
        node2 = Node(**base2.model_dump())
    except ValidationError as e:
        print('A Node can´t have extra fields')
        # print(e.json())
        
    class objEnum(EnumBase):
        @property
        def base_type(self):
            return self._get_class.base_type()
        @property
        def children(self):
            return self._get_class.children() 
    
    enum = make_enum(BaseObj, objEnum)
    
    e1: objEnum = enum.node
    print(e1.base_type)
    print(e1.children)
    node3 = e1.make(**base.model_dump())
    
    e2: objEnum = enum.item
    print(e2.base_type)
    print(e2.children)
    try:
        node4 = e2.make(**base.model_dump())
    except ValidationError as e:
        print('A Node cannot be casted to an Item')
        # print(e.json())
    
    attr = {
        'name': 'RBELLI',
        'id': '1234567890123456',
        'itemattr': 'field1node',
    }
    basei = BaseObj(**attr)
    node5 = e2.make(**basei.model_dump())
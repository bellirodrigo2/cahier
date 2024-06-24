from functools import partial
from typing import Generator, Type

from pydantic import BaseModel, field_validator, Field,  AliasGenerator
from pydantic import ConfigDict, ValidationError, AnyUrl
from pydantic.alias_generators import to_camel

from cahier.schemas.webid import WebId, make_webid
from cahier.schemas.makeenums import make_enum, EnumBase

from cahier.schemas.config import get_schema_settings

##############################################################################

SPECIAL_CHARS = ['*', '?', ';', '{', '}', '[', ']', '|', '\\', '`', ''', ''', ':']
INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add('/')

def make_name(name) -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{name}{i}"
        i += 1

settings = get_schema_settings()

name_gen = make_name(settings.default_name)

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
            )

NameField = partial(Field,
        description="Name Field Description",
        min_length=settings.name_min_length,
        max_length=settings.name_max_length,
    ),

DescriptionField = partial(Field,
        description="Description Field Description",
        min_length=settings.description_min_length,
        max_length=settings.description_max_length,
    ),

WebIdField = partial(Field, 
                    description="WebId Field Description",
                    default_factory=make_webid
                    )

ClientIdField = partial(Field, 
                    description="ClientId Field Description",
                    min_length=settings.clientid_min_length,
                    max_length=settings.clientid_max_length,
                    )

# webid eh criado qdo objinput ->obj.... mas qdo DB -> Obj, nap...ai é obrigatorio
    # compensa fazer webid obrigatorio e deixar o make_webid em uma factory ?
    # fazer dependencia de WEBID....injetar dependencia
# OBJ = OBJINPUT + WEBID..... TODOS OS FIELD SAO OPCIONAIS MAS TEM DEFAULT_FACTORY
# OBJUPDATE  TODOS OS FIELD SAO OPCIONAIS, NAO TEM DEFAULT
# SINGLEOUTPUT, IDEM OBJUPDATE + WEBID

# fazer- obj de baseclass....com extra para classes derivadas... mas depois nao pode mais ter extra...
# nas classes derivadas, da pra override o ConfigDict ???
# testar se mandar mais fields para AF...tipo {Name: zzz, Description:deddw, NonexistantField:foobar}
# testar dois niveis de cast.... para baseclass objinput por exemplo... e em um segundo nivel... classe derivada
# 

KeywordsField = partial(Field,
        description=''
        # por min e max do tmanho das strings
        )

class BaseInputObj(BaseModel):
    
    @classmethod
    def base_type(cls) -> str:
        return 'base'

    @classmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra='allow') #to allow derived class casting

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    client_id: str | None = ClientIdField(default_factory=make_webid)
    description: str | None = DescriptionField(default=settings.default_description)
    keywords: list[str] | None = KeywordsField(default=[])

class BaseObj(BaseInputObj):
    webid: WebId = WebIdField()

class BaseUpdate(BaseModel):
    model_config = ObjConfig(extra='allow')
    
    name: str | None = NameField(default=None)
    description: str | None = DescriptionField(default=None)
    keywords: list[str] | None = KeywordsField(default=None)
    
class BaseOutput(BaseUpdate):
    
    client_id: str | None = ClientIdField()
    webid: WebId | None = WebIdField()

class hasLinks:
    links: list[AnyUrl] = Field()
    
class SingleOutput(BaseOutput, hasLinks):
    pass

class ListOutput(hasLinks):
    list_: list[BaseOutput]

##############################################################################
class BaseServer(BaseInputObj):
    @classmethod
    def base_type(cls) -> str:
        return 'server'

    @classmethod
    def children(cls) -> list[str]:
        return ['root']

    model_config = ObjConfig(extra='forbid')
    
class BaseRoot(BaseInputObj):
    @classmethod
    def base_type(cls) -> str:
        return 'root'

    @classmethod
    def children(cls) -> list[str]:
        return ['element', 'node']

    model_config = ObjConfig(extra='forbid')

class BaseElement(BaseInputObj):
    @classmethod
    def base_type(cls) -> str:
        return 'element'

    @classmethod
    def children(cls) -> list[str]:
        return []

    model_config = ObjConfig(extra='forbid')
    
class BaseNode(BaseInputObj):
    @classmethod
    def base_type(cls) -> str:
        return 'node'

    @classmethod
    def children(cls) -> list[str]:
        return ['node', 'item', 'element']
    
    path: str = 'THIS_NODE_PATH'

    model_config = ObjConfig(extra='forbid')

class BaseItem(BaseInputObj):
    @classmethod
    def base_type(cls) -> str:
        return 'item'

    @classmethod
    def children(cls) -> list[str]:
        return ['item']
    
    path: str = 'THIS_NODE_PATH'

    model_config = ObjConfig(extra='forbid')
    

##############################################################################

class EnumBaseInputObj(EnumBase):
    @property
    def base_type(self):
        return self._get_class.base_type()
    @property
    def children(self):
        return self._get_class.children() 
    
ObjEnum: Type[EnumBaseInputObj] = make_enum(BaseInputObj, EnumBaseInputObj)
    
def is_valid_parent(parent: EnumBaseInputObj, child: EnumBaseInputObj):
    return child .base_type in parent.children

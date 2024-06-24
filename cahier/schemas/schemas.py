""" """

from typing import Annotated, Any, Generator
from functools import partial
from abc import ABC, abstractmethod

from pydantic import (AnyUrl, BaseModel, BeforeValidator, ConfigDict, Field,
                      field_validator, AliasGenerator)

from pydantic.alias_generators import to_camel

from cahier.schemas.webid import WebId, make_webid
from cahier.schemas.config import get_schema_settings

###############################################################################

settings = get_schema_settings()

SPECIAL_CHARS = ['*', '?', ';', '{', '}', '[', ']', '|', '\\', '`', ''', ''', ':']
INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add(settings.path_delim)

def make_name(name) -> Generator[str, None, None]:
    i = 0
    while True:
        yield f"{name}{i}"
        i += 1


name_gen = make_name(settings.default_name)


def check_invalid_char(name) -> str:
    for c in INVALID_CHARS:
        if c in name:
            raise ValueError(f"invalid charater {c=} in name: {name=}.")
    return name


# strip_str = BeforeValidator(lambda x: str.strip(str(x)))


def make_clientid():
    return str(make_webid())


###############################################################################

NameField = partial(Field,
        description="Name Field Description",
        min_length=settings.name_min_length,
        max_length=settings.name_max_length,
        # default_factory=lambda: next(name_gen),
    ),

DescriptionField = partial(Field,
        description="Description Field Description",
        min_length=settings.description_min_length,
        max_length=settings.description_max_length,
        default=settings.default_description,
    ),

ClientIdField = partial(Field, 
                    description="ClientId Field Description",
                    min_length=settings.clientid_min_length,
                    max_length=settings.clientid_max_length,
                    )
# 
# ClientIdField = Annotated[str | None, ClientIdFieldFunc(default_factory=make_clientid)]
# ClientIdFieldNone = Annotated[str | None, ClientIdFieldFunc()]

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

# AttributeField = Annotated[
    # dict[str, Any],
    # Field(
        # description="", 
        # default={}
    # ),
# ]

KeywordsField = partial(Field,
        description='',
        default=[],
        # por min e max do tmanho das strings
        )


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

class ObjInput(BaseModel, ABC):
    
    model_config = ObjConfig(extra='allow') #to allow derived class casting
    
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        pass

    name: str | None = NameField(default_factory=lambda: next(name_gen))
    description: str | None = DescriptionField(default=settings.default_description)
    client_id: str | None = ClientIdField(default_factory=make_clientid)
    keywords: list[str] | None= KeywordsField(default=[])

    @field_validator("name")
    @classmethod
    def check_special_char(_, name: str) -> str:
        return check_invalid_char(name)


class ObjUpdate(BaseModel):
    
    model_config = ObjConfig(extra='allow')
    
    name: str | None = NameField(default=None)
    description: str | None = DescriptionField(default=None)
    # client_id: str | None = ClientIdField(default=None, frozen=True)
    # attributes: AttributeField
    keywords: list[str] | None = KeywordsField(default=None)

WebIdField = Annotated[WebId,Field(default_factory=make_webid,)]

class Obj(ObjInput):
    web_id: WebIdField


class ObjOutput(ObjUpdate, ):
    web_id: WebIdField


class hasLinks:
    links: Annotated[
        list[AnyUrl], Field(
            default=[])
    ]


class SingleOutput(Obj, hasLinks):
    pass


class ListOutput(BaseModel, hasLinks):
    list_: Annotated[
        list[Obj],
        Field(
            # alias="List",
            # serialization_alias="List",
            default=[]
        ),
    ]

if __name__ == '__main__':

    from typing import Protocol    
    class base(Protocol):
        
        def hello(self, name: str | bool)->str | None:
            pass
        
    def run_func(base: base, x: str | bool):
        return base.hello(x)
    
    class der1:
        def hello(self, name: str)->str:
            return name.lower()
        
    class der2:
        def hello(self, name: base)->None:
            return name
            
    d1 = der1()
    d2 = der2()
    
    print(run_func(d1, 'gre'))
    print(run_func(d2, True))
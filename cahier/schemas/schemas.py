""" """
from typing import Annotated, Generator, List, Any

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, AnyUrl
from pydantic import field_validator, field_serializer

from .webid import WebId, hasWebId, make_webid

SPECIAL_CHARS = ['*', '?', ';', '{', '}', '[', ']', '|', '\\', '`', "'", '"', ':']
PATH_DELIM = '/'
DEFAULT_NAME = 'newNode'
NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 128
DEFAULT_DESCRIPTION = ''
DESCRIPTION_MIN_LENGTH = 0
DESCRIPTION_MAX_LENGTH = 512
CLIENTID_MIN_LENGTH = 4
CLIENTID_MAX_LENGTH = 64


################################################################################

INVALID_CHARS = set(SPECIAL_CHARS)
INVALID_CHARS.add(PATH_DELIM)


def make_name(name)->Generator[str, None, None]:
    i = 0
    while True:
        yield f'{name}{i}'
        i += 1


name_gen = make_name(DEFAULT_NAME)

def check_invalid_char(name)->str:
    for c in INVALID_CHARS:
            if c in name:
                raise ValueError(f'invalid charater {c=} in name: {name=}.')
    return name
    
    
strip_str = BeforeValidator(lambda x: str.strip(str(x)))

def make_clientid():
    return make_webid()

################################################################################

NameField = Annotated[str, strip_str , Field(
        description='Name Field Description',
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        alias='Name',
        validation_alias='Name',
        default_factory=lambda: next(name_gen),
    )]

DescriptionField = Annotated[str, strip_str, Field(
        description='Description Field Description',
        min_length=DESCRIPTION_MIN_LENGTH,
        max_length=DESCRIPTION_MAX_LENGTH,
        alias='Description',
        validation_alias='Description',
        default=DEFAULT_DESCRIPTION,
    )]

ClientIdField = Annotated[str, strip_str, Field(
        description='ClientId Field Description',
        min_length=CLIENTID_MIN_LENGTH,
        max_length=CLIENTID_MAX_LENGTH,
        alias='Id',
        validation_alias='Id',
        default=make_clientid,
    )]

AttributeField = Annotated[dict[str, Any], Field(
        description='',
        alias='Attributes',
        serialization_alias='Attributes',
        default={}
    )]

MetadataField = Annotated[dict[str, Any], Field(
        alias='Metadata',
        serialization_alias='Metadata',
        default={}
        )]

class ObjBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
        frozen=True,
        )

class ObjInput(ObjBaseModel):
    
    name: NameField
    description: DescriptionField
    client_id: ClientIdField
    attributes: AttributeField
    metadata: MetadataField
        
    @field_validator("name")
    @classmethod
    def check_special_char(_, name: str) -> str:
        return check_invalid_char(name)


class ObjUpdate(ObjBaseModel):
    name: NameField | None = None
    description: DescriptionField | None = None
    client_id: ClientIdField | None = None
    attributes: AttributeField | None = None
    metadata: MetadataField | None = None

class Obj(ObjInput, hasWebId):
    pass
    
class ObjOutput(ObjUpdate):    
    pass


class hasLinks:
    links: Annotated[list[AnyUrl], Field(
        alias='Links',
        serialization_alias='Links',
        default=[]
        )]
    

class SingleOutput(Obj, hasLinks):
    pass


class ListOutput(BaseModel, hasLinks):
    list_: Annotated[list[Obj], Field(
        alias='List',
        serialization_alias='List',    
    )]
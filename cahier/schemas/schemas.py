""" """

from typing import Annotated, Any, Generator

from pydantic import (AnyUrl, BaseModel, BeforeValidator, ConfigDict, Field,
                      field_validator, AliasGenerator)

from pydantic.alias_generators import to_camel

from cahier.schemas.webid import WebId, hasWebId, make_webid
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


strip_str = BeforeValidator(lambda x: str.strip(str(x)))


def make_clientid():
    return str(make_webid())


###############################################################################

NameField = Annotated[
    str,
    strip_str,
    Field(
        description="Name Field Description",
        min_length=settings.name_min_length,
        max_length=settings.name_max_length,
        # alias="Name",
        # validation_alias="Name",
        default_factory=lambda: next(name_gen),
    ),
]

DescriptionField = Annotated[
    str,
    strip_str,
    Field(
        description="Description Field Description",
        min_length=settings.description_min_length,
        max_length=settings.description_max_length,
        # alias="Description",
        # validation_alias="Description",
        default=settings.default_description,
    ),
]

ClientIdField = Annotated[
    str,
    strip_str,
    Field(
        description="ClientId Field Description",
        min_length=settings.clientid_min_length,
        max_length=settings.clientid_max_length,
        default_factory=make_clientid,
    ),
]

AttributeField = Annotated[
    dict[str, Any],
    Field(
        description="", 
        default={}
    ),
]

KeywordsField = Annotated[
    list[str], Field(
        description='',
        default=[])
]


class ObjBaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            alias=to_camel,
            validation_alias=to_camel,
            serialization_alias=to_camel
            ),
        populate_by_name=True,
        use_enum_values=True,
        frozen=True,
    )


class ObjInput(ObjBaseModel):

    name: NameField
    description: DescriptionField
    client_id: ClientIdField
    attributes: AttributeField
    keywords: KeywordsField

    @field_validator("name")
    @classmethod
    def check_special_char(_, name: str) -> str:
        return check_invalid_char(name)


class ObjUpdate(ObjBaseModel):
    name: NameField | None = None
    description: DescriptionField | None = None
    client_id: ClientIdField | None = None
    attributes: AttributeField | None = None
    keywords: KeywordsField | None = None


class Obj(ObjInput, hasWebId):
    pass


class ObjOutput(ObjUpdate):
    pass


class hasLinks:
    links: Annotated[
        list[AnyUrl], Field(alias="Links", serialization_alias="Links", default=[])
    ]


class SingleOutput(Obj, hasLinks):
    pass


class ListOutput(BaseModel, hasLinks):
    list_: Annotated[
        list[Obj],
        Field(
            alias="List",
            serialization_alias="List",
        ),
    ]

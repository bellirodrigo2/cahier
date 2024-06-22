""""""

from typing import Annotated

from pydantic import BaseModel, Field

###############################################################################


class FilterOptions(BaseModel):

    selected_fields: Annotated[
        list[str] | None,
        Field(
            description='List of fields to be returned in the response. For nested fields use "." (It can be list defined or one string separated by colons). Ex: {List.WebId:List.Value}',
            alias="selectedFields",
            validation_alias="selectedFields",
        ),
    ]

    field_filter: Annotated[
        list[str] | None,
        Field(
            description="filter field equal to value. use {Field:Target}. ex: Name:TargetName or Id:123456",
            alias="fieldFilter",
            validation_alias="fieldFilter",
        ),
    ]

    field_filter_like: Annotated[
        list[str] | None,
        Field(
            description='same as "fieldFilter" but with "has" instead of equal (like SQL "LIKE" keyword)',
            alias="fieldFilterLike",
            validation_alias="fieldFilterLike",
        ),
    ]

    metadata: Annotated[
        list[str] | None,
        Field(
            description=" Filter if the object has the given metadata",
            alias="Metadata",
            validation_alias="Metadata",
        ),
    ]

    template_name: Annotated[
        str | None,
        Field(
            description="Specify that returned attributes must be members of this template.",
            alias="templateName",
            validation_alias="templateName",
        ),
    ]

    search_full_hierarchy: Annotated[
        bool | None,
        Field(
            description="Specifies if the search should include attributes nested further than the immediate attributes of the searchRoot.",
            alias="searchFullHierarchy",
            validation_alias="searchFullHierarchy",
        ),
    ]

    sort_field: Annotated[
        str | None,
        Field(
            description="The field or property of the object used to sort the returned collection. Order can be defined as {FieldName:Asc} or {FieldName:Desc}",
            alias="sortField",
            validation_alias="sortField",
        ),
    ]

    start_index: Annotated[
        int | None,
        Field(
            description="The starting index (zero based) of the items to be returned.",
            alias="startIndex",
            validation_alias="startIndex",
        ),
    ]

    max_count: Annotated[
        int | None,
        Field(
            description="The starting index (zero based) of the items to be returned.",
            alias="maxCount",
            validation_alias="maxCount",
        ),
    ]

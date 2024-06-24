"""Cahier Object WebId type."""

# from typing import Annotated
from uuid import UUID, uuid1

# from pydantic import Field

###############################################################################

WebId = UUID


def make_webid() -> WebId:
    return uuid1()


# class hasWebId:
#     web_id: Annotated[
#         WebId,
#         Field(
#             alias="WebId",
#             serialization_alias="WebId",
#             frozen=True,
#             default_factory=make_webid,
#         ),
#     ]

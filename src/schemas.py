from enum import Enum

from pydantic import BaseModel


class TypeEnum(str, Enum):
    REPOSITORIES = "Repositories"
    ISSUES = "Issues"
    WIKIS = "Wikis"


class SearchParams(BaseModel):
    keywords: list[str]
    type: TypeEnum
    proxies: list[str]

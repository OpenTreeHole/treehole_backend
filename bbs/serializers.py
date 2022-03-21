from typing import Optional

from pydantic import BaseModel, Field

from bbs.models import Division
from utils.common import models_creator

DivisionModel, DivisionList = models_creator(Division)


class DivisionAdd(BaseModel):
    name: str = Field(max_length=16)
    description: Optional[str] = Field(max_length=100)


class DivisionModify(DivisionAdd):
    pinned: Optional[list[int]]


class DivisionDelete(BaseModel):
    to: int = Field(default=1)

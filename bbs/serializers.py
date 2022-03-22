from typing import Optional

from pydantic import BaseModel, Field

from bbs.models import Division
from utils.common import models_creator

DivisionS, DivisionListS = models_creator(Division)


class DivisionModel(BaseModel):
    name: str = Field(max_length=16)
    description: Optional[str] = Field(max_length=100, default='')
    pinned: Optional[list[int]] = Field(default=[])


class DivisionDelete(BaseModel):
    to: int = Field(default=1)

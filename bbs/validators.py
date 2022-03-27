from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, constr

from config import config


class DivisionModel(BaseModel):
    name: str = Field(max_length=16)
    description: Optional[str] = Field(max_length=100, default='')
    pinned: Optional[list[int]] = []


class DivisionDelete(BaseModel):
    to: Optional[int] = 1


class TagAdd(BaseModel):
    name: constr(min_length=1, max_length=16, strip_whitespace=True)


class FloorContent(BaseModel):
    content: constr(min_length=1, strip_whitespace=True)


class FloorAdd(FloorContent):
    hole_id: int
    special_tag: Optional[str] = ''


class FloorGetHole(BaseModel):
    offset: int = Field(default=0, ge=0)
    size: int = Field(default=config.default_size, ge=0)


class FloorGetHoleOld(BaseModel):
    hole_id: int
    offset: int = Field(default=0, ge=0, alias='start_floor')
    size: int = Field(default=config.default_size, ge=0, alias='length')


class HoleListSimple(BaseModel):
    # default_factory 在query校验中暂不支持，需要在 api 中设置默认值
    # start_time: Optional[datetime] = Field(default_factory=now)
    start_time: Optional[datetime]
    size: int = Field(
        default=config.default_size,
        le=config.default_size, ge=0,
        alias='length'
    )

    class Config:
        allow_population_by_field_name = True


class HoleList(HoleListSimple):
    tag: Optional[str]
    division_id: Optional[int] = 0


class HoleAdd(FloorContent):
    tags: List[TagAdd] = []


class HoleAddOld(HoleAdd):
    division_id: int = 1

from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Union

from pydantic import BaseModel, Field
from tortoise.queryset import QuerySet

from bbs.models import Division, Hole, Floor
from utils.orm import models_creator, OrmModel
from utils.values import LENGTH

DivisionS, DivisionListS = models_creator(Division)
HoleS, HoleListS = models_creator(Hole, exclude=('mapping',))
FloorS, FloorListS = models_creator(Floor, exclude=('mapping',))


class TagModel(OrmModel):
    name: str
    temperature: int


class SimpleFloorModel(OrmModel):
    id: int
    hole_id: int
    content: str
    anonyname: str
    time_created: datetime
    time_updated: datetime
    like: int
    deleted: bool
    fold: List[str]
    special_tag: str
    storey: int


class FloorModel(SimpleFloorModel):
    mention: List[SimpleFloorModel]
    liked: bool = False
    is_me: bool = False


async def serialize_floor(obj: Union[Floor, QuerySet[Floor]]) -> Union[dict, List[dict]]:
    def _construct_model(floor: Floor, user_id: int = 1) -> FloorModel:
        # todo: user
        floor._mention = floor.mention.related_objects
        floor.liked = user_id in floor.like_data
        floor.is_me = floor.user_id == user_id
        return FloorModel.from_orm(floor)

    if isinstance(obj, Floor):
        await obj.fetch_related('mention')
        return _construct_model(obj).dict()
    if isinstance(obj, QuerySet):
        floors = await obj.prefetch_related('mention')
        return [_construct_model(floor).dict() for floor in floors]
    return {}


class HoleFloor(BaseModel):
    first_floor: Optional[SimpleFloorModel]
    last_floor: Optional[SimpleFloorModel]
    prefetch: List[SimpleFloorModel]


class HoleModel(OrmModel):
    id: int
    division_id: int
    time_created: datetime
    time_updated: datetime
    reply: int
    view: int
    hidden: bool
    tags: List[TagModel]
    floors: HoleFloor


async def serialize_hole(obj: Union[Hole, QuerySet[Hole]]) -> Union[dict, List[dict]]:
    async def _construct_model(hole: Hole, user_id: int = 1) -> HoleModel:
        # todo: user
        hole._tags = hole.tags.related_objects
        floor_queryset = Floor.filter(hole_id=hole.pk)
        prefetch = await floor_queryset.limit(10)
        holefloor = HoleFloor(
            prefetch=prefetch,
            first_floor=prefetch[0] if prefetch else None,
            last_floor=await floor_queryset.order_by('-id').first()
        ),
        hole._floors = holefloor[0]
        return HoleModel.from_orm(hole)

    if isinstance(obj, Hole):
        await obj.fetch_related('tags')
        return (await _construct_model(obj)).dict()
    if isinstance(obj, QuerySet):
        holes = await obj.prefetch_related('tags')
        return [(await _construct_model(hole)).dict() for hole in holes]
    return {}


class DivisionModel(BaseModel):
    name: str = Field(max_length=16)
    description: Optional[str] = Field(max_length=100, default='')
    pinned: Optional[list[int]] = []


class DivisionDelete(BaseModel):
    to: Optional[int] = 1


class TagAdd(BaseModel):
    name: str


class FloorAdd(BaseModel):
    hole_id: int
    content: str
    special_tag: Optional[str] = ''


class FloorGetHole(BaseModel):
    offset: int = Field(default=0, ge=0, alias='start_floor')
    size: int = Field(default=LENGTH, ge=0, alias='length')

    class Config:
        allow_population_by_field_name = True


class HoleListGet(BaseModel):
    division_id: int = 1
    # default_factory 在query校验中暂不支持
    # start_time: datetime = Field(default_factory=now)
    start_time: Optional[datetime]
    length: int = Field(default=LENGTH, le=LENGTH, ge=0)
    tag: Optional[str]


class HoleAdd(BaseModel):
    division_id: int = 1
    content: str
    tags: List[TagAdd] = []

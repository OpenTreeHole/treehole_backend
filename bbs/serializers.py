from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from bbs.models import Division, Hole, Floor
from utils.orm import models_creator, OrmModel
from utils.values import now, LENGTH

DivisionS, DivisionListS = models_creator(Division)
HoleS, HoleListS = models_creator(Hole, exclude=('mapping',))
FloorS, FloorListS = models_creator(Floor, exclude=('mapping',))


class TagModel(OrmModel):
    name: str
    temperature: int


class HoleFloor(BaseModel):
    first_floor: FloorS
    last_floor: FloorS
    prefetch: List[FloorS]


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


async def serialize_hole(hole: Hole) -> dict:
    await hole.fetch_related('tags')
    hole._tags = hole.tags.related_objects
    floors = Floor.filter(hole_id=hole.pk)
    prefetch = await floors.limit(10)
    holefloor = HoleFloor(
        prefetch=prefetch,
        first_floor=prefetch[0],
        last_floor=await floors.order_by('-id').first()
    ),
    hole._floors = holefloor[0]
    model = HoleModel.from_orm(hole)
    return model.dict()


class DivisionModel(BaseModel):
    name: str = Field(max_length=16)
    description: Optional[str] = Field(max_length=100, default='')
    pinned: Optional[list[int]] = []


class DivisionDelete(BaseModel):
    to: int = Field(default=1)


class TagAdd(BaseModel):
    name: str


class FloorAdd(BaseModel):
    hole_id: int
    content: str
    special_tag: str = ''


class HoleListGet(BaseModel):
    division_id: int = 1
    start_time: datetime = Field(default_factory=now)
    length: int = Field(default=LENGTH, le=LENGTH, ge=0)
    tag: Optional[str]


class HoleAdd(BaseModel):
    division_id: int = 1
    content: str
    tags: List[TagAdd] = []

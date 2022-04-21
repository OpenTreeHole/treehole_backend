from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, create_model
from tortoise.queryset import MODEL

from bbs.models import Division, Hole, Floor, Tag
from utils.orm import models_creator, OrmModel, Serializer

TagModel, _ = models_creator(Tag)
DivisionS, DivisionListS = models_creator(Division)
HoleS, HoleListS = models_creator(Hole, exclude=('mapping',))
SimpleFloorModel, _ = models_creator(Floor)

SimpleFloorModel = create_model('SimpleFloorModel', hole_id=(int, ...), __base__=SimpleFloorModel)


class FloorModel(SimpleFloorModel, Serializer):
    mention: List[SimpleFloorModel]
    liked: bool = False
    is_me: bool = False

    @staticmethod
    def construct_model(floor: Floor, user_id: int = 1) -> MODEL:
        # todo: user
        floor._mention = floor.mention.related_objects
        floor.liked = user_id in floor.like_data
        floor.is_me = floor.user_id == user_id
        return floor


class HoleFloor(BaseModel):
    first_floor: Optional[SimpleFloorModel]
    last_floor: Optional[SimpleFloorModel]
    prefetch: List[SimpleFloorModel]


class HoleModel(OrmModel, Serializer):
    id: int
    division_id: int
    time_created: datetime
    time_updated: datetime
    reply: int
    view: int
    hidden: bool
    tags: List[TagModel]
    floors: HoleFloor
    
    @staticmethod
    async def construct_model(hole: Hole, user_id: int = 1) -> Hole:
        # todo: user
        hole._tags = hole.tags.related_objects
        floor_queryset = Floor.filter(hole_id=hole.pk)
        prefetch = await floor_queryset.limit(10)
        hole_floor = HoleFloor(
            prefetch=prefetch,
            first_floor=prefetch[0] if prefetch else None,
            last_floor=await floor_queryset.order_by('-id').first()
        ),
        hole._floors = hole_floor[0]
        return HoleModel.from_orm(hole)

from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from fastapi.logger import logger
from pydantic import create_model
from tortoise.queryset import MODEL

from bbs.models import Hole, Floor, Tag, Division
from user.models import User, anonymous_user
from utils.common import order_in_given_order
from utils.orm import Serializer, pmc, OrmModel

TagModel = pmc(Tag)
SimpleFloorModel = pmc(Floor)

SimpleFloorModel = create_model('SimpleFloorModel', hole_id=(int, ...), __base__=SimpleFloorModel)


class FloorModel(SimpleFloorModel, Serializer):
    mention: List[SimpleFloorModel]
    liked: bool = False
    disliked: bool = False
    is_me: bool = False

    class Config:
        related = ['mention']

    @staticmethod
    def construct_model(floor: Floor, user: User = anonymous_user) -> MODEL:
        if not user.pk:
            logger.warn('no user passed to serialize()')
        floor._mention = floor.mention.related_objects
        floor.liked = user.pk in floor.like_data
        floor.disliked = user.pk in floor.dislike_data
        floor.is_me = floor.user_id == user.pk
        return floor


class HoleFloor(OrmModel):
    first_floor: Optional[SimpleFloorModel]
    last_floor: Optional[SimpleFloorModel]
    prefetch: List[SimpleFloorModel]


class HoleModel(Serializer):
    id: int
    division_id: int
    time_created: datetime
    time_updated: datetime
    reply: int
    view: int
    hidden: bool
    tags: List[TagModel]
    floors: HoleFloor

    class Config:
        related = ['tags']

    @staticmethod
    async def construct_model(hole: Hole, **kwargs) -> Hole:
        hole._tags = hole.tags.related_objects
        floor_queryset = Floor.filter(hole_id=hole.pk)
        prefetch = await floor_queryset.limit(10)
        hole._floors = HoleFloor(
            prefetch=prefetch,
            first_floor=prefetch[0] if prefetch else None,
            last_floor=await floor_queryset.order_by('-id').first()
        )
        return hole


class DivisionModel(Serializer):
    id: int
    name: str
    description: str
    pinned: List[HoleModel]

    @staticmethod
    async def construct_model(division: Division, **kwargs) -> Division:
        holes = Hole.filter(id__in=division.pinned)
        holes = await HoleModel.serialize(holes)
        holes = order_in_given_order(holes, division.pinned)
        division.pinned = holes
        return division

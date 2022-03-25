from typing import List

from fastapi import APIRouter, Request, Depends

from bbs.models import Hole, Floor
from bbs.serializers import FloorAdd, serialize_floor, FloorGetHole, FloorModel
from user.models import User
from utils.common import find_mentions, random_name
from utils.orm import get_object_or_404

router = APIRouter(tags=['floor'])


@router.get('/holes/{hole_id}/floors', response_model=List[FloorModel])
async def list_floors_in_a_hole(hole_id: int, query: FloorGetHole = Depends()):
    queryset = Floor.filter(hole_id=hole_id).offset(query.offset)
    if query.size > 0:
        queryset = queryset.limit(query.size)
    return await serialize_floor(queryset)


@router.post('/floors', response_model=FloorModel, status_code=201)
async def add_a_floor(request: Request, body: FloorAdd):
    floor, hole = await inner_add_a_floor(
        request=request,
        body=body,
        hole=await get_object_or_404(Hole, id=body.hole_id)
    )
    return await serialize_floor(floor)


async def inner_add_a_floor(request: Request, body: FloorAdd, hole: Hole) -> [Floor, Hole]:
    user, created = await User.get_or_create(id=1)  # TODO: user
    anonyname = hole.mapping.get(str(user.pk))  # dict key must be a str
    if not anonyname:
        anonyname = random_name(hole.mapping.values())
        hole.mapping[str(user.pk)] = anonyname
    hole.reply += 1
    await hole.save()
    floor = await Floor.create(
        hole=hole,
        content=body.content,
        anonyname=anonyname,
        user=user,
        special_tag=body.special_tag,
        storey=hole.reply
    )
    mentions = await find_mentions(body.content)
    await floor.mention.add(*mentions)
    # TODO: 提及回复的发送通知

    return floor, hole

from typing import List

from fastapi import APIRouter, Request, Depends

from bbs.models import Hole, Floor
from bbs.serializers import FloorModel
from bbs.validators import FloorAdd, FloorGetHole, FloorGetHoleOld, FloorAddOld
from dependency import get_user
from user.models import User
from utils.common import find_mentions, random_name, get_ip_location, get_ip
from utils.orm import get_object_or_404

router = APIRouter(tags=['floor'])


############
#   GET
############
@router.get('/holes/{hole_id}/floors', response_model=List[FloorModel])
async def list_floors_in_a_hole(hole_id: int, query: FloorGetHole = Depends(), user: User = Depends(get_user)):
    queryset = Floor.filter(hole_id=hole_id).offset(query.offset)
    if query.size > 0:
        queryset = queryset.limit(query.size)
    return await FloorModel.serialize(queryset, user=user)


@router.get('/floors', deprecated=True, response_model=List[FloorModel])
async def list_floors_old(query: FloorGetHoleOld = Depends()):
    queryset = Floor.filter(hole_id=query.hole_id).offset(query.offset)
    if query.size > 0:
        queryset = queryset.limit(query.size)
    return await FloorModel.serialize(queryset)


############
#   POST
############
@router.post('/holes/{hole_id}/floors', response_model=FloorModel, status_code=201)
async def add_a_floor(request: Request, hole_id: int, body: FloorAdd):
    floor, hole = await inner_add_a_floor(
        request=request,
        body=body,
        hole=await get_object_or_404(Hole, id=hole_id)
    )
    return await FloorModel.serialize(floor)


@router.post('/floors', deprecated=True, response_model=FloorModel, status_code=201)
async def add_a_floor_old(request: Request, body: FloorAddOld):
    floor, hole = await inner_add_a_floor(
        request=request,
        body=body,
        hole=await get_object_or_404(Hole, id=body.hole_id)
    )
    return await FloorModel.serialize(floor)


async def inner_add_a_floor(request: Request, body: FloorAdd, hole: Hole) -> [Floor, Hole]:
    user, created = await User.get_or_create(id=1)  # TODO: user
    anonyname = hole.mapping.get(str(user.pk))  # dict key must be a str
    if not anonyname:
        anonyname = random_name(hole.mapping.values())
        hole.mapping[str(user.pk)] = anonyname
    hole.reply += 1
    await hole.save()
    floor: Floor = await Floor.create(
        hole=hole,
        content=body.content,
        anonyname=anonyname,
        user=user,
        special_tag=body.special_tag,
        storey=hole.reply,
        ip_location=get_ip_location(ip=get_ip(request))
    )
    mentions: List[Floor] = await find_mentions(body.content)
    await floor.mention.add(*mentions)
    # TODO: ???????????????????????????

    return floor, hole

############
#   PUT
############

############
#   DELETE
############

from sanic import Blueprint, Request

from bbs.models import Hole, Floor
from bbs.serializers import FloorAdd, FloorModel, serialize_floor, FloorGetHole
from user.models import User
from utils import myopenapi
from utils.common import find_mentions, random_name
from utils.orm import get_object_or_404
from utils.sanic_patch import json
from utils.validator import validate

bp = Blueprint('floor')


@bp.get('/holes/<hole_id:int>/floors')
@myopenapi.response(200, [FloorModel.construct()])
@myopenapi.query(FloorGetHole)
@validate(query=FloorGetHole)
async def list_floors_in_a_hole(request: Request, query: FloorGetHole, hole_id: int):
    queryset = Floor.filter(hole_id=hole_id).offset(query.offset)
    if query.size > 0:
        queryset = queryset.limit(query.size)
    return json(await serialize_floor(queryset))


@bp.post('/floors')
@myopenapi.response(201, FloorModel.construct())
@myopenapi.body(FloorAdd)
@validate(json=FloorAdd)
async def add_a_floor(request: Request, body: FloorAdd):
    floor, hole = await inner_add_a_floor(
        request=request,
        body=body,
        hole=await get_object_or_404(Hole, id=body.hole_id)
    )
    return json(await serialize_floor(floor))


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

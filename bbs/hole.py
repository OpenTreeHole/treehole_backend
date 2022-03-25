from sanic import Blueprint, Request

from bbs.floor import inner_add_a_floor
from bbs.models import Hole, Tag
from bbs.serializers import HoleListGet, HoleAdd, FloorAdd, serialize_hole, HoleModel
from utils import myopenapi
from utils.orm import get_object_or_404
from utils.sanic_patch import json
from utils.validator import validate

bp = Blueprint('hole')


@bp.get('/holes')
@myopenapi.response(200, [HoleModel])
@myopenapi.query(HoleListGet)
@validate(query=HoleListGet)
async def list_holes(request: Request, query: HoleListGet):
    if query.tag:
        tag = await get_object_or_404(Tag, name=query.tag)
        queryset = tag.holes.all()
    else:
        queryset = Hole.all()
    queryset = queryset.order_by('-time_updated').filter(
        time_updated__lt=query.start_time,
        division_id=query.division_id
    ).limit(query.length)
    return json(await serialize_hole(queryset))


@bp.get('/holes/<id:int>')
@myopenapi.response(200, HoleModel)
async def get_a_hole(request: Request, id: int):
    hole = await get_object_or_404(Hole, id=id)
    return json(await serialize_hole(hole))


@bp.post('/holes')
@myopenapi.response(200, HoleModel)
@myopenapi.body(HoleAdd)
@validate(json=HoleAdd)
async def add_a_hole(request: Request, body: HoleAdd):
    hole = await Hole.create(division_id=body.division_id)
    for tag_add in body.tags:
        tag, created = await Tag.get_or_create(name=tag_add.name)
        await hole.tags.add(tag)
    floor, hole = await inner_add_a_floor(
        request=request,
        body=FloorAdd(hole_id=hole.pk, content=body.content),
        hole=hole
    )
    return json(await serialize_hole(hole))

from typing import List

from fastapi import APIRouter, Request, Depends

from bbs.floor import inner_add_a_floor
from bbs.models import Hole, Tag
from bbs.serializers import HoleListGet, HoleAdd, FloorAdd, serialize_hole, HoleModel
from utils.orm import get_object_or_404
from utils.values import now

router = APIRouter(tags=['hole'])


@router.get('/holes', response_model=List[HoleModel])
async def list_holes(query: HoleListGet = Depends()):
    # 在 query 中使用模型要加 =Depends()
    if not query.start_time:
        query.start_time = now()
    if query.tag:
        tag = await get_object_or_404(Tag, name=query.tag)
        queryset = tag.holes.all()
    else:
        queryset = Hole.all()
    queryset = queryset.order_by('-time_updated').filter(
        time_updated__lt=query.start_time,
        division_id=query.division_id
    ).limit(query.length)
    return await serialize_hole(queryset)


@router.get('/holes/{id}', response_model=HoleModel)
async def get_a_hole(id: int):
    hole = await get_object_or_404(Hole, id=id)
    return await serialize_hole(hole)


@router.post('/holes', response_model=HoleModel, status_code=201)
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
    return await serialize_hole(hole)

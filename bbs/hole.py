from typing import List

from fastapi import APIRouter, Request, Depends
from tortoise.expressions import F
from tortoise.transactions import atomic

from bbs.floor import inner_add_a_floor
from bbs.models import Hole, Tag
from bbs.serializers import serialize_hole, HoleModel
from bbs.validators import FloorAdd, HoleListSimple, HoleList, HoleAdd, HoleAddOld
from utils.orm import get_object_or_404
from utils.values import now

router = APIRouter(tags=['hole'])


@router.get('/divisions/{division_id}/holes', response_model=List[HoleModel])
async def list_holes_by_division(division_id: int, query: HoleListSimple = Depends()):
    # 在 query 中使用模型要加 =Depends()
    if not query.start_time:
        query.start_time = now()
    queryset = Hole.all()
    if division_id != 0:
        queryset = queryset.filter(division_id=division_id)
    queryset = queryset.order_by('-time_updated').filter(
        time_updated__lt=query.start_time,
    ).limit(query.size)
    return await serialize_hole(queryset)


@router.get('/holes', response_model=List[HoleModel])
async def list_holes_by_tag(query: HoleList = Depends()):
    if not query.start_time:
        query.start_time = now()
    if query.tag:
        tag = await get_object_or_404(Tag, name=query.tag)
        queryset = tag.holes.all()
    else:
        queryset = Hole.all()
    if query.division_id != 0:
        queryset = queryset.filter(division_id=query.division_id)
    queryset = queryset.order_by('-time_updated').filter(
        time_updated__lt=query.start_time,
    ).limit(query.size)
    return await serialize_hole(queryset)


@router.get('/holes/{id}', response_model=HoleModel)
async def get_a_hole(id: int):
    hole = await get_object_or_404(Hole, id=id)
    return await serialize_hole(hole)


@router.post('/divisions/{division_id}/holes', response_model=HoleModel, status_code=201)
async def add_a_hole(request: Request, body: HoleAdd, division_id: int):
    hole = await inner_add_a_hole(request, division_id, body.content, body.tags)
    return await serialize_hole(hole)


@router.post('/holes', deprecated=True, response_model=HoleModel, status_code=201)
async def add_a_hole_old(request: Request, body: HoleAddOld):
    hole = await inner_add_a_hole(request, body.division_id, body.content, body.tags)
    return await serialize_hole(hole)


@atomic()
async def inner_add_a_hole(
        request: Request,
        division_id: int,
        content: str,
        tags: list
) -> Hole:
    hole = await Hole.create(division_id=division_id)
    added_tags = []
    for tag_add in tags:
        tag, created = await Tag.get_or_create(name=tag_add.name)
        added_tags.append(tag)
    await hole.tags.add(*added_tags)
    await hole.tags.all().update(temperature=F('temperature') + 1)
    floor, hole = await inner_add_a_floor(
        request=request,
        body=FloorAdd(hole_id=hole.pk, content=content),
        hole=hole
    )
    return hole

from sanic import Blueprint, Request

from bbs.models import Division, Hole
from bbs.serializers import DivisionList, DivisionAdd, DivisionModel, DivisionModify, DivisionDelete
from utils import myopenapi
from utils.common import json, get_object_or_404, exists_or_404
from utils.exceptions import BadRequest
from utils.validator import validate

bp = Blueprint('division')


@bp.get('/divisions')
@myopenapi.response(200, [DivisionModel.construct()])
async def list_divisions(request: Request):
    divisions = await DivisionList.from_queryset(Division.all())
    return json(divisions.json())


@bp.post('/divisions')
@myopenapi.body(DivisionAdd)
@myopenapi.response(201, DivisionModel.construct())
@validate(json=DivisionAdd)
async def add_division(request: Request, body: DivisionAdd):
    if await Division.filter(name=body.name).exists():
        raise BadRequest(f'分区名称“{body.name}”重复')
    division = await Division.create(**body.dict())
    division = await DivisionModel.from_tortoise_orm(division)
    return json(division.dict(), 201)


@bp.put('/divisions/<id:int>')
@myopenapi.body(DivisionModify)
@myopenapi.response(200, DivisionModel.construct())
@validate(json=DivisionModify)
async def modify_division(request: Request, body: DivisionModify, id: int):
    division = await get_object_or_404(Division, id=id)
    division.name = body.name or division.name
    division.description = body.description or division.description
    division.pinned = body.pinned or division.pinned
    await division.save()
    return json((await DivisionModel.from_tortoise_orm(division)).dict())


@bp.delete('/divisions/<id:int>')
@myopenapi.body(DivisionDelete)
@myopenapi.response(204, None)
@validate(json=DivisionDelete)
async def delete_division(request: Request, body: DivisionDelete, id: int):
    await exists_or_404(Division, id=id)
    await exists_or_404(Division, id=body.to)
    await Hole.filter(division_id=id).update(division_id=body.to)
    await Division.filter(id=id).delete()
    return json({}, 204)
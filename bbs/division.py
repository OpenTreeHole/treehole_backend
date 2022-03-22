from sanic import Blueprint, Request

from bbs.models import Division, Hole
from bbs.serializers import DivisionListS, DivisionModel, DivisionS, DivisionDelete
from utils import myopenapi
from utils.common import json, get_object_or_404, exists_or_404, serialize
from utils.validator import validate

bp = Blueprint('division')


@bp.get('/divisions')
@myopenapi.response(200, [DivisionS.construct()])
async def list_divisions(request: Request):
    return json(await serialize(Division.all(), DivisionListS))


@bp.get('/divisions/<id:int>')
@myopenapi.response(200, DivisionS.construct())
async def get_a_division(request: Request, id: int):
    division = await get_object_or_404(Division, id=id)
    return json(await serialize(division, DivisionS))


# @bp.get('/divisions/<id:int>/pinned')
# @myopenapi.response(200, DivisionS.construct())
# async def get_a_division(request: Request, id: int):
#     division = await get_object_or_404(Division, id=id)
#
#     return json(await serialize(division, DivisionS))


@bp.post('/divisions')
@myopenapi.response(201, DivisionS.construct())
@myopenapi.body(DivisionModel)
@validate(json=DivisionModel)
async def add_division(request: Request, body: DivisionModel):
    division = await Division.create(**body.dict())
    return json(await serialize(division, DivisionS), 201)


@bp.put('/divisions/<id:int>')
@myopenapi.response(200, DivisionS.construct())
@myopenapi.body(DivisionModel)
@validate(json=DivisionModel)
async def modify_division(request: Request, body: DivisionModel, id: int):
    division = await Division.get_or_none(id=id)
    if not division:
        d = body.dict()
        d['id'] = id
        division = await Division.create(**d)
    else:
        division.name = body.name or division.name
        division.description = body.description or division.description
        division.pinned = body.pinned or division.pinned
        await division.save()
    return json(await serialize(division, DivisionS))


@bp.delete('/divisions/<id:int>')
@myopenapi.response(204, None)
@myopenapi.body(DivisionDelete)
@validate(json=DivisionDelete)
async def delete_division(request: Request, body: DivisionDelete, id: int):
    await exists_or_404(Division, id=id)
    await exists_or_404(Division, id=body.to)
    await Hole.filter(division_id=id).update(division_id=body.to)
    await Division.filter(id=id).delete()
    return json(None, 204)

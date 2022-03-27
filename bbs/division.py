from typing import List

from fastapi import APIRouter

from bbs.models import Division, Hole
from bbs.serializers import DivisionListS, DivisionS
from bbs.validators import DivisionModel, DivisionDelete
from utils.exceptions import BadRequest
from utils.orm import get_object_or_404, exists_or_404, serialize

router = APIRouter(tags=['division'])


@router.get('/divisions', response_model=List[DivisionS])
async def list_divisions():
    return await serialize(Division.all(), DivisionListS)


@router.get('/divisions/{id}', response_model=DivisionS)
async def get_a_division(id: int):
    division = await get_object_or_404(Division, id=id)
    return await serialize(division, DivisionS)


# @bp.get('/divisions/<id:int>/pinned')
# @myopenapi.response(200, DivisionS.construct())
# async def get_a_division(request: Request, id: int):
#     # todo: 获取置顶帖列表
#     division = await get_object_or_404(Division, id=id)
#
#     return json(await serialize(division, DivisionS))


@router.post('/divisions', response_model=DivisionS, status_code=201)
async def add_division(body: DivisionModel):
    if await Division.filter(name=body.name).exists():
        raise BadRequest(f'Division name {body.name} exists')
    division = await Division.create(**body.dict())
    return await serialize(division, DivisionS)


@router.put('/divisions/{id}', response_model=DivisionS)
async def modify_division(body: DivisionModel, id: int):
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
    return await serialize(division, DivisionS)


@router.delete('/divisions/{id}', status_code=204)
async def delete_division(body: DivisionDelete, id: int):
    await exists_or_404(Division, id=id)
    await exists_or_404(Division, id=body.to)
    await Hole.filter(division_id=id).update(division_id=body.to)
    await Division.filter(id=id).delete()
    return None

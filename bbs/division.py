from typing import List

from fastapi import APIRouter

from bbs.models import Division, Hole
from bbs.serializers import DivisionModel
from bbs.validators import DivisionAdd, DivisionDelete
from utils.exceptions import BadRequest
from utils.orm import get_object_or_404, exists_or_404

router = APIRouter(tags=['division'])


@router.get('/divisions', response_model=List[DivisionModel])
async def list_divisions():
    return await DivisionModel.serialize(Division.all())


@router.get('/divisions/{id}', response_model=DivisionModel)
async def get_a_division(id: int):
    division = await get_object_or_404(Division, id=id)
    return await DivisionModel.serialize(division)


@router.post('/divisions', response_model=DivisionModel, status_code=201)
async def add_division(body: DivisionAdd):
    if await Division.filter(name=body.name).exists():
        raise BadRequest(f'Division name {body.name} exists')
    division = await Division.create(**body.dict())
    return await DivisionModel.serialize(division)


@router.put('/divisions/{id}', response_model=DivisionModel)
async def modify_division(body: DivisionAdd, id: int):
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
    return await DivisionModel.serialize(division)


@router.delete('/divisions/{id}', status_code=204)
async def delete_division(body: DivisionDelete, id: int):
    await exists_or_404(Division, id=id)
    await exists_or_404(Division, id=body.to)
    await Hole.filter(division_id=id).update(division_id=body.to)
    await Division.filter(id=id).delete()
    return None

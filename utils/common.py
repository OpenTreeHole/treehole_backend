from typing import Type, Tuple, Union

import orjson
import sanic
from sanic import HTTPResponse
from sanic.exceptions import NotFound
from tortoise import Model
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_queryset_creator, \
    pydantic_model_creator
from tortoise.queryset import QuerySet


def dumps_str(*args, **kwargs) -> str:
    return orjson.dumps(*args, **kwargs).decode('utf-8')


def json(data, *args) -> HTTPResponse:
    if isinstance(data, str):
        return sanic.json(data, *args, dumps=lambda x: x)
    else:
        return sanic.json(data, *args, dumps=dumps_str)


def models_creator(cls: Type[Model]) -> Tuple[Type[PydanticModel], Type[PydanticListModel]]:
    return pydantic_model_creator(cls), pydantic_queryset_creator(cls)


async def get_object_or_404(cls: Type[Model], *args, **kwargs) -> Model:
    instance = await cls.get_or_none(*args, **kwargs)
    if not instance:
        raise NotFound(f'{cls.__name__} does not exist')
    return instance


async def exists_or_404(cls: Type[Model], *args, **kwargs) -> bool:
    if not await cls.filter(*args, **kwargs).exists():
        raise NotFound(f'{cls.__name__} does not exist')
    return True


async def serialize(obj: Union[Model, QuerySet], cls: Union[PydanticModel, PydanticListModel]) -> dict:
    if isinstance(obj, Model):
        return (await cls.from_tortoise_orm(obj)).dict()
    elif isinstance(obj, QuerySet):
        model = await cls.from_queryset(obj)
        return model.dict()['__root__']

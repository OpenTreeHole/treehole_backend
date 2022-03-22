from functools import wraps
from inspect import isawaitable
from typing import Optional
from urllib.parse import unquote

from pydantic import BaseModel, ValidationError
from sanic import Request

from utils.exceptions import BadRequest


def do_validate(model: type[BaseModel], data: dict, kwargs: dict, param_name='body'):
    data = data or {}
    try:
        body = model(**data)
    except ValidationError as e:
        message = ''
        for error in e.errors():
            message += f'{", ".join(error["loc"])} {error["msg"]}\n'
        raise BadRequest(message.strip())
    kwargs[param_name] = body


def validate(
        json: Optional[type[BaseModel]] = None,
        match: Optional[type[BaseModel]] = None,
        query: Optional[type[BaseModel]] = None
):
    """
    自定义校验，校验成功的模型出现在 api 函数的参数中，失败返回 400，有 message

    Args:
        json: 校验 json，参数名 body
        match: 校验 url 截取 (e.g. /verify/<email:str>), 参数名 match
        query: 校验 query params，参数名 query

    Returns:
        装饰器
    """

    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            if json:
                data = request.json
                # no_id = 'id' not in data
                # if no_id:
                #     data['id'] = 1
                do_validate(json, data, kwargs, 'body')
                # if no_id and hasattr(kwargs['body'], 'id'):
                #     del kwargs['body'].id
            if match:
                match_info = request.match_info
                for key in match_info:
                    if isinstance(match_info[key], str):
                        match_info[key] = unquote(match_info[key])
                do_validate(match, match_info, kwargs, 'match')
            if query:
                for key in request.args:
                    if len(request.args[key]) == 1:
                        request.args[key] = request.args[key][0]  # 数组展开
                do_validate(query, request.args, kwargs, 'query')
            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response
            return response

        return decorated_function

    return decorator

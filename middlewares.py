import time

import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from config import config
from user.models import User
from utils.exceptions import Forbidden
from utils.patch import MyFastAPI

app = MyFastAPI.get_app()

if config.debug:
    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = f'{process_time * 1000:.1f} ms'
        return response

token_scheme = HTTPBearer(auto_error=False)


async def get_user(token: HTTPAuthorizationCredentials = Depends(token_scheme)):
    if config.debug:
        user, _ = await User.get_or_create(id=1)
        payload = {'is_admin': True, 'config': {}, 'nickname': ''}
    else:
        payload = jwt.decode(token.credentials, options={"verify_signature": False})
        user, _ = await User.get_or_create(id=payload.get('uid'))

    user.is_admin = payload.get('is_admin')
    user.config = payload.get('config')
    user.nickname = payload.get('nickname')
    return user


async def admin_only(user: User = Depends(get_user)):
    if not user.is_admin:
        raise Forbidden('admin only')

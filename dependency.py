import jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from config import config
from user.models import User
from utils.exceptions import Forbidden
from utils.patch import MyFastAPI

app = MyFastAPI.get_app()

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

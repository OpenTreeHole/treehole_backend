from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()  # app 实例化位于所有导入之前
from bbs import division, floor, hole
from utils.common import get_ip

app.include_router(division.router)
app.include_router(floor.router)
app.include_router(hole.router)


@app.get('/')
async def home(request: Request):
    return {
        'message': 'hello world',
        'ip': get_ip(request)
    }

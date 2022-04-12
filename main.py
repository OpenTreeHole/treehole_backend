from fastapi import FastAPI, Request

app = FastAPI()  # app 实例化位于所有导入之前
from bbs import division, floor, hole

app.include_router(division.router)
app.include_router(floor.router)
app.include_router(hole.router)


@app.get('/')
async def home(request: Request):
    for (k, v) in request.headers.items():
        k: str
        if k.lower().startswith('x'):
            print(k, v)
    return {'message': 'hello world'}

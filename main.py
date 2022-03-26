from fastapi import FastAPI

app = FastAPI()  # app 实例化位于所有导入之前
from bbs import division, floor, hole

app.include_router(division.router)
app.include_router(floor.router)
app.include_router(hole.router)


@app.get('/')
async def home():
    return {'message': 'hello world'}

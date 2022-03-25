from fastapi import FastAPI
# from sanic import Request, json
# from tortoise.exceptions import IntegrityError
#
# from config import app
#
# print(app)
# from bbs.division import bp as division
# from bbs.floor import bp as floor
# from bbs.hole import bp as hole
# from utils.exceptions import integrity_error_handler
#
# app.blueprint([division, hole, floor])
#
# app.error_handler.add(IntegrityError, integrity_error_handler)
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()  # app 实例化位于所有导入之前
from bbs import division
from config import TORTOISE_ORM

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)
app.include_router(division.router)


@app.get('/')
async def home():
    return {'message': 'hello world'}

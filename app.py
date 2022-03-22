import multiprocessing

from sanic import Request, json
from tortoise.exceptions import IntegrityError

from config import app

print(app)
from bbs.division import bp as division
from bbs.floor import bp as floor
from bbs.hole import bp as hole
from utils.exceptions import integrity_error_handler

app.blueprint([division, hole, floor])

app.error_handler.add(IntegrityError, integrity_error_handler)


@app.get('/')
async def home(request: Request):
    return json({'message': 'hello world'})


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        workers=app.config.get('WORKERS', multiprocessing.cpu_count()),
        debug=app.config['DEBUG'],
        access_log=app.config['DEBUG']
    )

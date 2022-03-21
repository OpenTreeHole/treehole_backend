import multiprocessing

from sanic import Request, json

from bbs.division import bp as division
from config import app

app.blueprint(division)


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

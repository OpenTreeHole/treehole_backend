import asyncio
import multiprocessing
import time

import uvicorn
from aerich import Command
from starlette.requests import Request

from bbs import division, floor, hole
from config import TORTOISE_ORM, config
from utils.common import get_ip
from utils.patch import MyFastAPI

app = MyFastAPI.get_app()
app.include_router(division.router)
app.include_router(floor.router)
app.include_router(hole.router)


@app.get('/')
async def home(request: Request):
    return {
        'message': 'hello world',
        'ip': get_ip(request)
    }


if config.debug:
    @app.middleware('http')
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = f'{process_time * 1000:.1f} ms'
        return response


async def migrate():
    command = Command(tortoise_config=TORTOISE_ORM)
    await command.init()
    await command.migrate()
    await command.upgrade()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(migrate())
    uvicorn.run(
        app='main:app', host='0.0.0.0', port=8000,
        workers=1 if config.debug else multiprocessing.cpu_count(),
        reload=config.debug,
        log_level='info'
    )

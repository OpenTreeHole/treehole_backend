from pyinstrument import Profiler
from starlette.requests import Request

from bbs import division, floor, hole
from config import config
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
    async def profile(request: Request, call_next):
        profiler = Profiler()
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        with open('data/profile.html', 'w', encoding='utf-8') as f:
            f.write(profiler.output_html())

        return response

import pytz
from pytz import UnknownTimeZoneError
from sanic import Sanic
from tortoise import Tortoise

app = Sanic('treehole')
app.config['MODE'] = MODE = app.config.get('MODE', 'dev')
app.config['DEBUG'] = (app.config['MODE'] != 'production')
try:
    app.config['TZ'] = pytz.timezone(app.config.get('TZ', 'UTC'))
except UnknownTimeZoneError:
    app.config['TZ'] = pytz.timezone('utc')
app.config.OAS_UI_DEFAULT = 'swagger'
app.config.FALLBACK_ERROR_FORMAT = 'json'

MODELS = ['user.models', 'bbs.models', 'admin.models']

TORTOISE_ORM = {
    'apps': {
        'models': {
            'models': MODELS + ['aerich.models']
        }
    },
    'connections': {  # aerich 暂不支持 sqlite
        'default': app.config.get('DB_URL', 'mysql://username:password@mysql:3306/treehole')
    },
    'use_tz': True,
    'timezone': str(app.config['TZ'])
}


@app.signal('server.init.after')
async def init(*args, **kwargs):
    if MODE != 'test':
        await Tortoise.init(TORTOISE_ORM)


@app.signal('server.shutdown.before')
async def close(*args, **kwargs):
    if MODE != 'test':
        await Tortoise.close_connections()


def get_sanic_app() -> Sanic:
    return app

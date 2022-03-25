from datetime import tzinfo

import pytz
from fastapi.openapi.utils import get_openapi
from pydantic import BaseSettings

from main import app


class Settings(BaseSettings):
    mode: str = 'dev'
    debug: bool = True
    tz: tzinfo = pytz.UTC
    db_url: str


config = Settings()

MODELS = ['user.models', 'bbs.models', 'admin.models']

TORTOISE_ORM = {
    'apps': {
        'models': {
            'models': MODELS + ['aerich.models']
        }
    },
    'connections': {  # aerich 暂不支持 sqlite
        'default': config.db_url
    },
    'use_tz': True,
    'timezone': str(config.tz)
}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title='OpenTreeHole Docs',
        version="2.0.0",
        description="OpenAPI doc for OpenTreeHole",
        routes=app.routes
    )

    # look for the error 422 and removes it
    for path in openapi_schema['paths'].values():
        for method in path:
            try:
                del path[method]['responses']['422']
            except KeyError:
                pass

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

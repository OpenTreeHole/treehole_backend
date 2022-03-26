from datetime import tzinfo
from typing import Optional

import pytz
from fastapi.openapi.utils import get_openapi
from pydantic import BaseSettings
from tortoise.contrib.fastapi import register_tortoise

from main import app


class Settings(BaseSettings):
    mode: str = 'dev'
    debug: bool = True
    tz: tzinfo = pytz.UTC
    db_url: str = 'sqlite://db.sqlite3'
    test_db: str = 'sqlite://:memory:'
    default_size: Optional[int] = 10


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

if config.mode != 'test':
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )


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

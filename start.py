import asyncio
import multiprocessing

import uvicorn
from aerich import Command
from tortoise import Tortoise

from config import TORTOISE_ORM, config, MODELS


async def migrate():
    command = Command(tortoise_config=TORTOISE_ORM)
    await command.init()
    await command.migrate()
    await command.upgrade()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(migrate())
    Tortoise.init_models(MODELS, 'models')
    uvicorn.run(
        app='main:app', host='0.0.0.0', port=8000,
        workers=1 if config.debug else multiprocessing.cpu_count(),
        reload=config.debug,
        log_level='info'
    )

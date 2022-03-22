from tortoise.contrib.test import TestCase

import utils.sanic_patch
from app import app


class TestHome(TestCase):

    async def test_get(self):
        req, res = await app.asgi_client.get('/')
        assert res.status == 200
        assert utils.sanic_patch.json == {'message': 'hello world'}

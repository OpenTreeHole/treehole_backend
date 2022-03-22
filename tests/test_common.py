from tortoise.contrib.test import TestCase

from app import app


class TestHome(TestCase):

    async def test_get(self):
        req, res = await app.asgi_client.get('/')
        assert res.status == 200
        assert res.json == {'message': 'hello world'}

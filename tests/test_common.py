from tortoise.contrib.test import TestCase

from tests.test_bbs import c


class TestHome(TestCase):

    async def test_get(self):
        res = c.get('/')
        assert res.status_code == 200
        assert res.json() == {'message': 'hello world'}

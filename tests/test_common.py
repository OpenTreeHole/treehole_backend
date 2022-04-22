from tortoise.contrib.test import TestCase

from . import c


class TestHome(TestCase):

    async def test_get(self):
        res = c.get('/')
        assert res.status_code == 200
        assert res.json() == {'ip': 'testclient', 'message': 'hello world'}

import pytest
from tortoise.contrib import test
from tortoise.contrib.test import finalizer, initializer

from app import app
from bbs.models import Division
from config import MODELS


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = app.config.get('TEST_DB', 'sqlite://:memory:')
    initializer(MODELS, db_url=db_url, app_label='models')
    request.addfinalizer(finalizer)


class TestDivision(test.TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        await Division.create(name='1')

    async def test_get(self):
        req, res = await app.asgi_client.get('/divisions/1')
        assert res.status == 200
        print(res.json)
        req, res = await app.asgi_client.get('/divisions')
        assert res.status == 200

    async def test_post(self):
        data = {
            'name': 'test_post_1',
        }
        req, res = await app.asgi_client.post('/divisions', json=data)
        assert res.status == 201

        data = {
            'name': 'test_post_1',
        }
        req, res = await app.asgi_client.post('/divisions', json=data)
        assert res.status == 400
        assert res.json['message'] == f'分区名称 test_post_1 重复'

        data = {
            'name': 'test_post_2',
            'description': 'description'
        }
        req, res = await app.asgi_client.post('/divisions', json=data)
        assert res.status == 201

        data = {
            'name': 'test_post_3',
            'description': 'description',
            'pinned': [1, 2, 3]
        }
        req, res = await app.asgi_client.post('/divisions', json=data)
        assert res.status == 201

    async def test_put(self):
        data = {
            'name': 'test_put',
            'description': 'description',
            'pinned': [1, 2]
        }
        req, res = await app.asgi_client.put('/divisions/1', json=data)
        assert res.status == 200
        assert res.json['id'] == 1
        del res.json['id']
        assert res.json == data

    async def test_delete(self):
        d = await Division.create(name='test_delete')
        req, res = await app.asgi_client.delete(f'/divisions/{d.pk}')
        assert res.status == 204
        assert await Division.filter(id=d.pk).exists() is False
    #
    # def test_order(self):
    #     division = Division.objects.create(name='name', pinned=[4, 2, 5])
    #     r = self.client.get(f'/divisions/{division.id}')
    #     ids = list(map(lambda hole: hole['hole_id'], r.json()['pinned']))
    #     self.assertEqual(ids, [4, 2, 5])

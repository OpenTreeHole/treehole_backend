import pytest
from tortoise.contrib import test
from tortoise.contrib.test import finalizer, initializer

from bbs.models import Division, Hole
from config import MODELS, config
from . import c


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(MODELS, db_url=config.test_db)
    request.addfinalizer(finalizer)


class TestDivision(test.TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        division = await Division.create(name='1')
        holes = []
        for i in range(3):
            holes.append(Hole(division=division))
        await Hole.bulk_create(holes)

    async def test_get(self):
        res = c.get('/divisions/1')
        assert res.status_code == 200
        res = c.get('/divisions')
        assert res.status_code == 200

    async def test_post(self):
        data = {
            'name': 'test_post_1',
        }
        res = c.post('/divisions', json=data)
        assert res.status_code == 201

        data = {
            'name': 'test_post_1',
        }
        res = c.post('/divisions', json=data)
        assert res.status_code == 400

        data = {
            'name': 'test_post_2',
            'description': 'description'
        }
        res = c.post('/divisions', json=data)
        assert res.status_code == 201

        data = {
            'name': 'test_post_3',
            'description': 'description',
            'pinned': [1, 2, 3]
        }
        res = c.post('/divisions', json=data)
        assert res.status_code == 201

    async def test_put(self):
        data = {
            'name': 'test_put',
            'description': 'description',
            'pinned': [1, 2]
        }
        res = c.put('/divisions/1', json=data)
        assert res.status_code == 200
        json = res.json()
        del json['id']
        json['pinned'] = list(map(lambda x: x['id'], json['pinned']))
        assert json == data

    async def test_delete(self):
        d = await Division.create(name='test_delete')
        res = c.delete(f'/divisions/{d.pk}', json={})
        assert res.status_code == 204
        assert await Division.filter(id=d.pk).exists() is False

    # def test_order(self):
    #     division = Division.objects.create(name='name', pinned=[4, 2, 5])
    #     r = self.client.get(f'/divisions/{division.id}')
    #     ids = list(map(lambda hole: hole['hole_id'], r.json()()['pinned']))
    #     self.assertEqual(ids, [4, 2, 5])

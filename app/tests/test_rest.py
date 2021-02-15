from http import HTTPStatus

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from app import rest


class RESTTestCase(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes([
            web.get('/api/values/{key}/', rest.handle_get_value),
            web.post('/api/values/{key}/', rest.handle_post_value)
        ])
        return app

    @unittest_run_loop
    async def test_get_value(self):
        test_key = 123
        test_value = "test value"

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.OK
        data = await resp.json()
        assert test_value in data

    @unittest_run_loop
    async def test_get_key_not_found(self):
        test_key = 321

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.NOT_FOUND

    @unittest_run_loop
    async def test_handle_post(self):
        test_key = 123

        resp = await self.client.request("POST", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.ACCEPTED

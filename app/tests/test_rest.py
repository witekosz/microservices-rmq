from http import HTTPStatus

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from unittest.mock import MagicMock

from app import rest


class RESTTestCase(AioHTTPTestCase):
    async def get_application(self):
        rpc_client = MagicMock()
        rpc_client.connect = MagicMock(return_value=rpc_client)
        rpc_client.send_simplex_message = MagicMock(return_value=None)
        rpc_client.send_simplex_message = MagicMock(return_value="test value")

        app = web.Application()
        app.add_routes(
            [
                web.get("/api/values/{key}/", rest.handle_get_value),
                web.post("/api/values/", rest.handle_post_value),
            ]
        )
        return app

    @unittest_run_loop
    async def test_get_value(self):
        test_key = "123"
        test_value = "test value"

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.OK
        data = await resp.json()
        assert test_value in data

    @unittest_run_loop
    async def test_get_key_not_found(self):
        test_key = "321"

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.NOT_FOUND

    @unittest_run_loop
    async def test_handle_post(self):
        test_key = "123"
        test_value = "test value"
        data = {"key": test_key, "value": test_value}

        resp = await self.client.request("POST", f"/api/values/", json=data)

        assert resp.status == HTTPStatus.ACCEPTED

    @unittest_run_loop
    async def test_handle_post_validation(self):

        resp = await self.client.request("POST", f"/api/values/", json={})

        assert resp.status == HTTPStatus.BAD_REQUEST
        data = await resp.json()
        assert {"message": "Validation error, pass valid: key"}

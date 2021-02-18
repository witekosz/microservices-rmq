import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, patch

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, TestServer, unittest_run_loop

from app import rest
from app.rpc_client import RPCServiceClient


class RESTTestCase(AioHTTPTestCase):
    async def get_application(self):
        rpc_client_mock = AsyncMock(RPCServiceClient)

        app = web.Application()
        app["rpc_client"] = await rpc_client_mock()
        app["rpc_client"].send_duplex_message.return_value = None
        app.add_routes(
            [
                web.get("/api/values/{key}/", rest.handle_get_value),
                web.post("/api/values/", rest.handle_post_value),
            ]
        )
        return app

    @unittest_run_loop
    async def test_get_key_not_found(self):
        test_key = "321"

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.NOT_FOUND

    @unittest_run_loop
    async def test_get_value(self):
        test_key = "123"
        test_value = "test value"
        self.app["rpc_client"].send_duplex_message.return_value = b"test value"

        resp = await self.client.request("GET", f"/api/values/{test_key}/")

        assert resp.status == HTTPStatus.OK
        resp_message = await resp.json()
        assert resp_message == {"key": test_key, "value": test_value}

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
        resp_message = await resp.json()
        assert resp_message == {
            "key": ["Missing data for required field."],
            "value": ["Missing data for required field."],
        }

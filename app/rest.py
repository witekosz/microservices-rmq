import asyncio
from http import HTTPStatus

from aiohttp import web
from marshmallow import Schema, ValidationError, fields

from app.rpc_client import RPCServiceClient


class ValueSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)


async def handle_get_value(request):
    key = request.match_info.get("key")

    data = await request.app["rpc_client"].send_duplex_message(key)

    if data:
        return web.json_response({"key": key, "value": data.decode("utf-8")})
    else:
        return web.json_response(status=HTTPStatus.NOT_FOUND)


async def handle_post_value(request):
    data = await request.json()

    try:
        message = ValueSchema().load(data)
    except ValidationError as exp:
        return web.json_response(
            exp.messages,
            status=HTTPStatus.BAD_REQUEST,
        )

    await request.app["rpc_client"].send_simplex_message(message)

    return web.json_response(status=HTTPStatus.ACCEPTED)


async def start_rpc_client(app):
    rpc_client = RPCServiceClient().connect()
    app["rpc_client"] = await asyncio.create_task(rpc_client)


async def end_rpc_client(app):
    await app["rpc_client"].connection.close()


app = web.Application()


app.add_routes(
    [
        web.get("/api/values/{key}/", handle_get_value),
        web.post("/api/values/", handle_post_value),
    ]
)

if __name__ == "__main__":
    app.on_startup.append(start_rpc_client)
    app.on_cleanup.append(end_rpc_client)
    web.run_app(app)

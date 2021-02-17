import asyncio
from http import HTTPStatus

from aiohttp import web

from rpc_client import send_duplex_message, RPCServiceClient
from send_client import send_simplex_message


app = web.Application()


async def handle_get_value(request):
    key = request.match_info.get("key")

    data = await send_duplex_message(key)

    if data:
        return web.json_response({"value": data.decode("utf-8")})
    else:
        return web.json_response(status=HTTPStatus.NOT_FOUND)


async def handle_post_value(request):
    try:
        data = await request.json()
        key = data["key"]
        value = data["value"]
    except KeyError as exp:
        return web.json_response(
            {"message": f"Validation error, pass valid: {exp}"},
            status=HTTPStatus.BAD_REQUEST,
        )

    await send_simplex_message(key=key, value=value)

    return web.json_response(status=HTTPStatus.ACCEPTED)


async def start_rpc_client(app):
    rpc_client = RPCServiceClient().connect()
    app['rpc_client'] = await asyncio.create_task(rpc_client)


async def end_rpc_client(app):
    await app['rpc_client'].connection.close()


app.add_routes(
    [
        web.get("/api/values/{key}/", handle_get_value),
        web.post("/api/values/", handle_post_value),
    ]
)

app.on_startup.append(start_rpc_client)
app.on_cleanup.append(end_rpc_client)
web.run_app(app)

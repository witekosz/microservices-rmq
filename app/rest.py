import asyncio
from http import HTTPStatus

from aiohttp import web

from rpc_client import send_duplex_message
from send_client import send_simplex_message


async def handle_get_value(request):
    key = request.match_info.get("key")

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(send_duplex_message(loop, key)),
    ]
    done, _ = await asyncio.wait(tasks)
    data = done.pop().result()

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

    loop = asyncio.get_event_loop()
    tasks = [
        asyncio.ensure_future(send_simplex_message(loop, key=key, value=value)),
    ]
    await asyncio.wait(tasks)

    return web.json_response(status=HTTPStatus.ACCEPTED)


app = web.Application()
app.add_routes(
    [
        web.get("/api/values/{key}/", handle_get_value),
        web.post("/api/values/", handle_post_value),
    ]
)


if __name__ == "__main__":
    web.run_app(app)

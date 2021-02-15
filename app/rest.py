from http import HTTPStatus

from aiohttp import web


async def handle_get_value(request):
    mock_value = {
        123: "test value"
    }
    # TODO Implement get from queue

    key = request.match_info.get("key")
    data = mock_value.get(int(key))
    if data:
        return web.json_response(data)
    else:
        return web.json_response(status=HTTPStatus.NOT_FOUND)


async def handle_post_value(request):
    key = request.match_info.get("key")
    # TODO Implement sending to queue
    return web.json_response(status=HTTPStatus.ACCEPTED)


app = web.Application()
app.add_routes([
    web.get('/api/values/{key}/', handle_get_value),
    web.post('/api/values/{key}/', handle_post_value)
])


if __name__ == '__main__':
    web.run_app(app)

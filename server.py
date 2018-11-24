from aiohttp import web
import json


async def handle(request):
    text = "Hello World!"
    return web.Response(text=text)


async def parse_media(request):
    data = await request.json()
    return web.json_response(data)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        web.post('/parse_media', parse_media),
    ])

    web.run_app(app)

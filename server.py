from aiohttp import web
import json
from crawlers import instagram


async def handle(request):
    text = "Hello World!"
    return web.Response(text=text)


async def parse_media(request):
    data = await request.json()
    url = data.get('url')
    if not url:
        return web.json_response(dict(status='error', message='url required'))
    result = await instagram.crawl(url=url)
    return web.json_response(dict(status='success', objects=result))


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        web.post('/parse_media', parse_media),
    ])

    web.run_app(app)

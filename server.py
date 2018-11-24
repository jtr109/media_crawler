from aiohttp import web

async def handle(request):
    text = "Hello World!"
    return web.Response(text=text)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        web.post('/parse_media', handle),
    ])

    web.run_app(app)

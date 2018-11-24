from aiohttp import web

async def handle(request):
    text = "Hello World!"
    return web.Response(text=text)

app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/parse_media', handle),
])

web.run_app(app)

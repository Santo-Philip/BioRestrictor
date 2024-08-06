import asyncio
from pyrogram import idle, Client
from aiohttp import web
from utils.mongo import Database
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

api_id = 1474940
api_hash = "779e8d2b32ef76d0b7a11fb5f132a6b6"
bot_token = "6513923912:AAHqD8O3NSIr2eZ27nqBt7uSKQfDHi4KgZk"
#bot_token = "7000419779:AAGMG1mWEpwQy_pKTzVRikRGfW1g6gKOETk"
plugins = dict(root='plugins')

async def handle(request):
    return web.Response(text="Hello, World!")

async def start_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    print(site)
    await site.start()

async def bot():
  app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins= plugins
    )
  await app.start()
  Database.initialize()
  await idle()


async def main():
  await asyncio.gather(start_server(),bot())
  
asyncio.run(main())
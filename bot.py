import asyncio
from pyrogram import idle, Client

from misc.periodic import period_check

api_id = 1474940
api_hash = "779e8d2b32ef76d0b7a11fb5f132a6b6"
bot_token = "5804042113:AAF_ynBaL_ZLcDQf6HwkKGEwrII72ZpKc3Y"


async def main():
    app = Client(
        "my_bot",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        plugins=dict(root='plugins')
    )
    await app.start()
    task = asyncio.create_task(period_check(app))
    await task
    await idle()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    loop = asyncio.get_event_loop()
    loop.stop()

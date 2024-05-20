import asyncio
from pyrogram import idle, Client

api_id = 1474940
api_hash = "779e8d2b32ef76d0b7a11fb5f132a6b6"
bot_token = "6513923912:AAEN9ISrYV8-ivtS9BNaq0hSh7HC0SUkWDk"
plugins = dict(root='plugins')

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token,
    plugins= plugins
)
app.run()

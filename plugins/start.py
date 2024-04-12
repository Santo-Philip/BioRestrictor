from pyrogram import filters, Client as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@app.on_message(filters.command("start"))
async def start(client, message):
    button = InlineKeyboardButton("Join our channel", url="https://t.me/BlazingSquad")
    keyboard = InlineKeyboardMarkup([[button]])
    startstr = ("🌟 Greetings! I am a modern Telegram bot here to assist you in maintaining a link-free "
                "environment.\n\n 🚨 Use /biowarn to elegantly warn users about their bio content. \n\n 🔨 Employ "
                "/bioban to gracefully ban users who persistently include links in their bios. \n\n🔇 Enhance order "
                "with /biomute to tactfully mute users. \n\n Let's keep the community thriving! \n\n 🤖 @BlazingSquad")
    await message.reply(text=startstr, reply_markup=keyboard)
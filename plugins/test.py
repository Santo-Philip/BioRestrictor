import asyncio
from datetime import datetime, timedelta
import re
from pyrogram import Client as app, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

link_pattern = re.compile(r'(?:https?://)?(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/(?:\+\w+|\w+)')
mention_pattern = re.compile(r'@((?!all)\w+)')


@app.on_message(filters.command('test', prefixes='/'))
async def testing(bot: app, msg):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Unmute Me", callback_data='unmute')]]
    )
    await msg.reply('test', reply_markup=keyboard)


@app.on_callback_query(filters.regex('unmute'))
async def unmute(bot: app, q: CallbackQuery):
    try:
        user = q.from_user.id
        member = await bot.get_chat_member(chat_id=-1001334989871, user_id=user)
        users = await bot.get_chat(chat_id=member.user.id)
        about = users.bio
        if about is not None:
            links = link_pattern.findall(about)
            plink = mention_pattern.findall(about)
            if plink:
                for link in plink:
                    chat = await bot.get_chat(chat_id=link)
                    if chat.type is not ChatType.PRIVATE:
                        initial_time = datetime.now()
                        time = initial_time + timedelta(hours=int(4))
                        await bot.restrict_chat_member(chat_id=q.message.chat.id, permissions=ChatPermissions(),
                                                       until_date=time, user_id=q.from_user.id)
                        await q.answer('Remove the link from bio')
                    await asyncio.sleep(3)
            if links:
                for link in links:
                    initial_time = datetime.now()
                    time = initial_time + timedelta(hours=int(4))
                    await bot.restrict_chat_member(chat_id=q.message.chat.id, permissions=ChatPermissions(),
                                                       until_date=time, user_id=q.from_user.id)
                    await q.answer('Remove the link from bio')
                await asyncio.sleep(3)
            if plink and links is None:
                await bot.restrict_chat_member(user_id=member.user.id,chat_id=q.message.chat.id,permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
                can_pin_messages=True,
                    can_send_polls=True,
                    can_change_info=True,
                    can_send_other_messages=True
                ))
                await  q.answer('You can now message')
        if about is None:
            await bot.restrict_chat_member(user_id=member.user.id, chat_id=q.message.chat.id,
                                           permissions=ChatPermissions(
                                               can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_add_web_page_previews=True,
                                               can_invite_users=True,
                                               can_pin_messages=True,
                                               can_send_polls=True,
                                               can_change_info=True,
                                               can_send_other_messages=True
                                           ))
            await  q.answer('You can now message')
    except UserNotParticipant:
        await q.answer('You have to join @BlazingSquad')

import asyncio
from datetime import datetime, timedelta
import re
from pyrogram import Client as app, filters
from pyrogram.enums import ChatType
from pyrogram.types import CallbackQuery, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MessageNotModified
from plugins.message import container

link_pattern = re.compile(r'(?:https?://)?(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/(?:\+\w+|\w+)')
mention_pattern = re.compile(r'@((?!all)\w+)')

channel = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Join Our Channel", url='https://t.me/BlazingSquad')],
     [InlineKeyboardButton('Try Again', 'unmute')]]
)

@app.on_message(filters.command('test'))
async def test(bot,msg):
    await msg.reply('hello')
@app.on_callback_query(filters.regex('unmute'))
async def unmute(bot: app, q: CallbackQuery):
    try:
        user = q.from_user.id
        member = await bot.get_chat_member(chat_id=-1001334989871, user_id=user)
        if user not in container:
            await q.answer('Not for you', show_alert=True)
            return
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
                        container.append(user)
                        await q.answer('Remove the link from bio')
                    else:
                        if user in container:
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
                            container.remove(user)
                            await q.answer('You can now message')
            if links:
                for _ in links:
                    initial_time = datetime.now()
                    time = initial_time + timedelta(hours=int(4))
                    await bot.restrict_chat_member(chat_id=q.message.chat.id, permissions=ChatPermissions(),
                                                   until_date=time, user_id=q.from_user.id)
                    container.append(user)
                    await q.answer('Remove the link from bio')
                await asyncio.sleep(3)
            if plink and links is None:
                if user in container:
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
                    container.remove(user)
                    await q.answer('You can now message')
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
            container.remove(user)
            await q.answer('You can now message')
    except UserNotParticipant:
        try:
            await q.message.edit_text(
                text=f"Dear {q.from_user.first_name} You have to be a prticipant of our official channel",
                reply_markup=channel)
        except MessageNotModified:
            await q.answer('Join our Channel to unmute')

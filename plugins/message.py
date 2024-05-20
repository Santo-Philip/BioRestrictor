import asyncio
import re
from datetime import datetime, timedelta
from pyrogram import Client as app, filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid, ChannelInvalid, \
    UsernameInvalid
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import MessageDeleteForbidden
from pyrogram.types import Message, ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton

link_pattern = re.compile(r'(?:https?://)?(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/(?:\+\w+|\w+)')
mention_pattern = re.compile(r'@((?!all)\w+)')
keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Unmute Me", callback_data='unmute')]]
)

container = []

@app.on_message((filters.media | filters.text | filters.document) & filters.group)
async def msg_check(client, message: Message):
    if message is None or message.from_user is None or message.from_user.is_bot:
        return

    user_id = message.from_user.id
    first = message.from_user.first_name
    last = message.from_user.last_name
    chat_id = message.chat.id
    mentions = (f"Dear... {first} {last if last else ''}\n🌟 Your profile has been flagged to administrators 🚩 due to "
                f"the presence of a link in your bio. "
                f"\n\n🎋Please remove it before taking any actions\n\n ID : {user_id}"
                f"\n\nUpdates : @BlazingSquad")
    links_store = f"[\u2063](tg://user?id={user_id})"
    mentions += "".join(links_store)
    try:
        if user_id is not None:
            user = await client.get_chat(chat_id=user_id)
            about = user.bio
            if about is not None:
                links = link_pattern.findall(about)
                plink = mention_pattern.findall(about)
                if plink:
                    initial_time = datetime.now()
                    time = initial_time + timedelta(hours=int(4))
                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                    await client.send_message(chat_id=chat_id, text=mentions,reply_markup=keyboard)
                    container.append(user_id)
                    await message.delete()
                if links:
                    initial_time = datetime.now()
                    time = initial_time + timedelta(hours=int(4))
                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                    await client.send_message(chat_id=chat_id, text=mentions,reply_markup=keyboard)
                    container.append(user_id)
                    await message.delete()
    except UserAdminInvalid:
        return
    except ChatAdminRequired:
        warn = await client.send_message(chat_id=chat_id, text=f"I don't have administrative privileges "
                                                               f"in this "
                                                               f"group, so I can't offer any services here.  "
                                                               f"\n\nIf "
                                                               f"this message seems incorrect, please report : "
                                                               f"@BlazingSquad")
        await asyncio.sleep(5)
        await warn.delete()
        return
    except FloodWait as f:
        await asyncio.sleep(f.value)
    except MessageDeleteForbidden:
        await client.send_message(chat_id=chat_id,
                                  text="Give Me Message deleting permission  \n\nIf this message "
                                       "seems incorrect, please report it : @BlazingSquad")
        return
    except ChannelInvalid:
        return
    except UsernameInvalid:
        return
    except Exception as e:
         print(e)
         await client.send_message(chat_id=chat_id, text=f"{e} \n\nReport : @BlazingSquad")
         return

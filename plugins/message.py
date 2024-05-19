import asyncio
from pyrogram import Client as app, filters
from pyrogram.types import ChatPermissions, Message
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelInvalid, UsernameInvalid, \
    UserAdminInvalid
from pyrogram.errors.exceptions.forbidden_403 import MessageDeleteForbidden
from pyrogram.errors.exceptions.flood_420 import FloodWait
from datetime import datetime, timedelta
import re

initial_time = datetime.now()
link_pattern = re.compile(r'(?:https?://)?(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/(?:\+\w+|\w+)')
mention_pattern = re.compile(r'@((?!all)\w+)')


@app.on_message((filters.media | filters.text | filters.document) & filters.group)
async def msg_check(client, message: Message):
    if message is None or message.from_user is None or message.from_user.is_bot:
        return
    time = initial_time + timedelta(hours=int(4))
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
            user = await client.resolve_peer(peer_id=user_id)
            user_detail = await client.invoke(
                GetFullUser(id=user)
            )
            await asyncio.sleep(3)
            about = user_detail.full_user.about
            if about is not None:
                links = link_pattern.findall(about)
                plink = mention_pattern.findall(about)
                if plink:
                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                    await client.send_message(chat_id=chat_id, text=mentions)
                    await message.delete()
                if links:
                    try:
                        await client.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                        await client.send_message(chat_id=chat_id, text=mentions)
                        await message.delete()
                    except UserAdminInvalid:
                        return
                    except ChatAdminRequired:
                        await client.send_message(chat_id=chat_id, text=f"I don't have administrative privileges "
                                                                        f"in this"
                                                                        f"group, so I can't offer any services here.  "
                                                                        f"\n\nIf"
                                                                        f"this message seems incorrect, please report : "
                                                                        f"@BlazingSquad")
                        await client.leave_chat(chat_id=chat_id)
                        return
                    except Exception as e:
                        await client.send_message(chat_id=chat_id, text=f"{e} \n\n Report : @BlazingSquad")
                        return
    except FloodWait as f:
        await asyncio.sleep(f.value)
    except MessageDeleteForbidden:
        await client.send_message(chat_id=chat_id, text="Give Me Message deleting permission  \n\nIf this message "
                                                        "seems incorrect, please report it : @BlazingSquad")
        return
    except ChannelInvalid:
        return
    except UsernameInvalid:
        return
    except ChatAdminRequired:
        await client.send_message(chat_id=chat_id,
                                  text=f"I don't have administrative privileges in this group, so I can't offer any"
                                       f"services here.  \n\nIf this message seems incorrect, please report : "
                                       f"@BlazingSquad")
        await client.leave_chat(chat_id=chat_id)
        return
    except UserAdminInvalid:
        return
    except Exception as e:
        print(e)
        await client.send_message(chat_id=chat_id, text=f"{e} \n\nReport : @BlazingSquad")
        return

import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw import functions
from pyrogram.errors import BadRequest
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, ChannelInvalid,UsernameInvalid
from pyrogram.errors.exceptions.forbidden_403 import MessageDeleteForbidden
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
import re

api_id = 1474940
api_hash = "779e8d2b32ef76d0b7a11fb5f132a6b6"
bot_token = "6513923912:AAEN9ISrYV8-ivtS9BNaq0hSh7HC0SUkWDk"

app = Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

initial_time = datetime.now()
link_pattern = re.compile(r'https?://(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/\+?\w+')
mention_pattern = re.compile(r'@((?!all)\w+)')

plink = ''
links = ''
userrr = ''
user = ''
user_id = ''


@app.on_message(filters.command(["biowarn", "bioban", "biomute"]) & filters.group)
async def biocmd(client, message):
    global plink, links, userrr, user_id
    chat_id = message.chat.id
    administrators = []
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m.user.id)
    if message.from_user.id in administrators:
        try:
            async for members in client.get_chat_members(chat_id):

                if message is not None and message.from_user is not None:
                    user_id = message.from_user.id
                if user_id is not None:
                    userrr = await app.resolve_peer(user_id)
                try:
                    ll = await app.invoke(
                        GetFullUser(
                            id=userrr
                        )
                    )
                    await asyncio.sleep(3)
                    about = ll.full_user.about
                    if about is not None:
                        links = link_pattern.findall(about)
                        plink = mention_pattern.findall(about)

                    if plink and user_id not in administrators:

                        try:
                            r = await app.invoke(
                                functions.channels.GetFullChannel(
                                    channel=await app.resolve_peer(plink[0])
                                )
                            )
                            await asyncio.sleep(3)
                            if r:
                                if message.command[0] == 'biowarn':
                                    member = await app.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Dear... {member.user.first_name} "
                                              f"{member.user.last_name if member.user.last_name else ''}"
                                              f"\n [ ](tg://user?id={user_id}) \n 🌟 We value your presence here, "
                                              f"but kindly note that adding links in the bio is not allowed in this "
                                              f"group. Let's keep the focus on engaging discussions. Thank you for "
                                              f"your cooperation! 🙌 \n\n #CommunityGuidelines \n\nUpdates : "
                                              f"@BlazingSquad")
                                    await app.send_message(chat_id, usrtxt)
                                if message.command[0] == 'biomute':
                                    await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
                                    member = await app.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Dear... {member.user.first_name} {member.user.last_name} \n[ ]("
                                              f"tg://user?id={user_id}) \n 🌟 We value your presence here, "
                                              f"but kindly note that adding links in the bio is not allowed in this "
                                              f"group. Let's keep the focus on engaging discussions. Thank you for "
                                              f"your cooperation! 🙌 \n\n#CommunityGuidelines \n\nUpdates : "
                                              f"@BlazingSquad")
                                    await app.send_message(chat_id, usrtxt)
                                if message.command[0] == 'bioban':
                                    await app.ban_chat_member(chat_id, user_id)
                                    member = await app.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Regrettably, {member.user.first_name} {member.user.last_name} has "
                                              f"faced a ban due to the inclusion of a link in the bio. 🚫 We "
                                              f"appreciate your understanding and cooperation in this matter. \n\n "
                                              f"#CommunityGuidelines \n\nUpdates : @BlazingSquad")
                                    await app.send_message(chat_id, usrtxt)

                        except BadRequest as b:
                            await app.send_message(chat_id=chat_id, text=f"{b.MESSAGE}  \n\nIf this message seems "
                                                                         f"incorrect, please report :"
                                                                         f"@BlazingSquad")
                            return
                        except Exception as e:
                            await app.send_message(chat_id=chat_id, text=f"{e}  \n\nIf this message seems "
                                                                         f"incorrect, please report :"
                                                                         f"@BlazingSquad")
                            return
                    if links and user_id not in administrators:
                        if message.command[0] == 'biowarn':
                            member = await app.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Dear... {member.user.first_name} "
                                      f"{member.user.last_name if member.user.last_name else ''} "
                                      f"\n[ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly "
                                      f"note that adding links in the bio is not allowed in this group. Let's keep "
                                      f"the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n "
                                      f"#CommunityGuidelines \n\nUpdates : @BlazingSquad")
                            await app.send_message(chat_id, usrtxt)
                        if message.command[0] == 'biomute':
                            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
                            member = await app.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Dear... {member.user.first_name} "
                                      f"{member.user.last_name}\n [ ](tg://user?id={user_id}) \n 🌟 We value your "
                                      f"presence here, but kindly note that adding links in the bio is not allowed in "
                                      f"this group. Let's keep the focus on engaging discussions. Thank you for your "
                                      f"cooperation! 🙌 \n\n #CommunityGuidelines \n\nUpdates : @BlazingSquad")
                            await app.send_message(chat_id, usrtxt)
                        if message.command[0] == 'bioban':
                            await app.ban_chat_member(chat_id, user_id)
                            member = await app.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Regrettably, {member.user.first_name} {member.user.last_name} has faced a ban "
                                      f"due to the inclusion of a link in the bio. 🚫 We appreciate your "
                                      f"understanding and cooperation in this matter. \n\n #CommunityGuidelines"
                                      f"\n\nUpdates : @BlazingSquad")
                            await app.send_message(chat_id, usrtxt)

                except Exception as e:
                    await message.reply(f"{e} "f"\n\nincorrect, please report :"
                                        f"@BlazingSquad")
                    print(e)
                    return
        except FloodWait as f:
            await asyncio.sleep(f.value)
        except UsernameInvalid:
            return
        except ChannelInvalid :
            return
        except Exception as e:
            print(e)
            await message.reply('I dont have enough permission to do this action ')
            return
    else:
        await message.reply('You have to be an admin to do this')
        return


@app.on_message(filters.command("start"))
async def start(client, message):
    button = InlineKeyboardButton("Join our channel", url="https://t.me/BlazingSquad")
    keyboard = InlineKeyboardMarkup([[button]])
    startstr = ("🌟 Greetings! I am a modern Telegram bot here to assist you in maintaining a link-free "
                "environment.\n\n 🚨 Use /biowarn to elegantly warn users about their bio content. \n\n 🔨 Employ "
                "/bioban to gracefully ban users who persistently include links in their bios. \n\n🔇 Enhance order "
                "with /biomute to tactfully mute users. \n\n Let's keep the community thriving! \n\n 🤖 @BlazingSquad")
    await message.reply(text=startstr, reply_markup=keyboard)


@app.on_message(filters.group & ~filters.left_chat_member)
async def msg_check(client, message):
    global plink, links, user, user_id
    time = initial_time + timedelta(hours=int(3))
    if message is not None and message.from_user is not None:
        user_id = message.from_user.id
    first = message.from_user.first_name
    last = message.from_user.last_name
    chat_id = message.chat.id
    administrators = []
    menid = [user_id]
    mentions = (f"Dear... {first} {last if last else ''}\n🌟 Your profile has been flagged to administrators 🚩 due to "
                f"the presence of a link in your bio. "
                f"\n\n🎋Please remove it before taking any actions\n\n ID : {user_id}"
                f"\n\nUpdates : @BlazingSquad")
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        menid.append(m.user.id)
        administrators.append(m.user.id)
    for id in menid:
        mentions += f"[\u2063](tg://user?id={id})"
    try:
        if user_id is not None:
            user = await app.resolve_peer(user_id)
        try:
            user_detail = await app.invoke(GetFullUser(id=user))
            await asyncio.sleep(3)
            about = user_detail.full_user.about
            if about is not None:
                links = link_pattern.findall(about)
                plink = mention_pattern.findall(about)
            if plink and user_id not in administrators:
                await message.delete()
                await app.invoke(functions.channels.GetFullChannel(channel=await app.resolve_peer(plink[0])))
                try:
                    await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                except Exception as e:
                    print(e)

                await app.send_message(chat_id, mentions)
            if links and user_id not in administrators:
                await message.delete()
                try:
                    await app.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
                except ChatAdminRequired:
                    await app.send_message(chat_id=chat_id, text=f"I don't have administrative privileges in this "
                                                                 f"group, so I can't offer any services here.  \n\nIf "
                                                                 f"this message seems incorrect, please report : "
                                                                 f"@BlazingSquad")
                    await app.leave_chat(chat_id=chat_id)
                    return
                except Exception as e:
                    await app.send_message(chat_id=chat_id, text=f"{e} \n\n Report : @BlazingSquad")
                    return
                await app.send_message(chat_id, mentions)
        except FloodWait as f:
            await asyncio.sleep(f.value)
        except MessageDeleteForbidden:
            await app.send_message(chat_id=chat_id, text="Give Me Message deleting permission  \n\nIf this message "
                                                         "seems incorrect, please report it : @BlazingSquad")
            return
        except ChannelInvalid:
            return
        except UsernameInvalid:
            return
        except ChatAdminRequired:
            await app.send_message(chat_id=chat_id,
                                   text=f"I don't have administrative privileges in this group, so I can't offer any "
                                        f"services here.  \n\nIf this message seems incorrect, please report : "
                                        f"@BlazingSquad")
            await app.leave_chat(chat_id=chat_id)
            return
        except Exception as e:
            print(e)
            await app.send_message(chat_id=chat_id, text=f"{e} \n\nReport : @BlazingSquad")
            return
    except Exception as e:
        print(e)
        await app.send_message(chat_id=chat_id, text=F"{e} \n\nReport : @BlazingSquad")
        return


try:
    app.run()
except KeyboardInterrupt:
    app.stop()

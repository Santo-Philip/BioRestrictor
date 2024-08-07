import asyncio
from pyrogram import Client as app, filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw import functions
from pyrogram.errors import BadRequest
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid
from pyrogram.errors.exceptions.flood_420 import FloodWait
from datetime import datetime
import re
from utils.mongo import Database
from config import LOG

initial_time = datetime.now()
link_pattern = re.compile(r'(?:https?://)?(?:t(?:elegram\.me|\.me|elegram\.dog)|telegram\.dog)/(?:\+\w+|\w+)')
mention_pattern = re.compile(r'@((?!all)\w+)')

plink = ''
links = ''


@app.on_message(filters.command(["biowarn", "bioban", "biomute"]) & filters.group)
async def biocmd(client, message):
    q = await message.reply('Please Wait checking users')
    global plink, links
    chat_id = message.chat.id
    exist = Database.fetchOneFrom('biogroup',chat_id,'user')
    if exist is None:
      data = {'user': chat_id}
      Database.insert('biogroup',data)
      await client.send_message(chat_id=LOG,text=f"__#NewGroup__\n\nGroup : `{chat_id}`\nName : {message.chat.title}")
    admins = []
    async for m in client.get_chat_members(chat_id=chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(m.user.id)
    if message.from_user.id in admins:
        try:
            async for members in client.get_chat_members(chat_id):
                user_id = members.user.id
                userrr = await client.resolve_peer(user_id)
                try:
                    ll = await client.invoke(
                        GetFullUser(
                            id=userrr
                        )
                    )
                    await asyncio.sleep(3)
                    about = ll.full_user.about
                    if about is not None:
                        links = link_pattern.findall(about)
                        plink = mention_pattern.findall(about)

                    if plink and user_id not in admins:

                        try:
                            r = await client.invoke(
                                functions.channels.GetFullChannel(
                                    channel=await client.resolve_peer(plink[0])
                                )
                            )
                            if r:
                                if message.command[0] == 'biowarn':
                                    member = await client.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Dear... {member.user.first_name} "
                                              f"{member.user.last_name if member.user.last_name else ''}"
                                              f"\n [ ](tg://user?id={user_id}) \n 🌟 We value your presence here, "
                                              f"but kindly note that adding links in the bio is not allowed in this "
                                              f"group. Let's keep the focus on engaging discussions. Thank you for "
                                              f"your cooperation! 🙌 \n\n #CommunityGuidelines \n\nUpdates : "
                                              f"@BlazingSquad")
                                    await client.send_message(chat_id, usrtxt)
                                if message.command[0] == 'biomute':
                                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                                    member = await client.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Dear... {member.user.first_name} {member.user.last_name} \n[ ]("
                                              f"tg://user?id={user_id}) \n 🌟 We value your presence here, "
                                              f"but kindly note that adding links in the bio is not allowed in this "
                                              f"group. Let's keep the focus on engaging discussions. Thank you for "
                                              f"your cooperation! 🙌 \n\n#CommunityGuidelines \n\nUpdates : "
                                              f"@BlazingSquad")
                                    await client.send_message(chat_id, usrtxt)
                                if message.command[0] == 'bioban':
                                    await client.ban_chat_member(chat_id, user_id)
                                    member = await client.get_chat_member(chat_id, user_id)
                                    usrtxt = (f"Regrettably, {member.user.first_name} {member.user.last_name} has "
                                              f"faced a ban due to the inclusion of a link in the bio. 🚫 We "
                                              f"appreciate your understanding and cooperation in this matter. \n\n "
                                              f"#CommunityGuidelines \n\nUpdates : @BlazingSquad")
                                    await client.send_message(chat_id, usrtxt)

                        except BadRequest as b:
                            await client.send_message(chat_id=chat_id, text=f"{b.MESSAGE}  \n\nIf this message seems "
                                                                            f"incorrect, please report :"
                                                                            f"@BlazingSquad")
                            return
                        except Exception as e:
                            await client.send_message(chat_id=chat_id, text=f"{e}  \n\nIf this message seems "
                                                                            f"incorrect, please report :"
                                                                            f"@BlazingSquad")
                            return
                    if links and user_id not in admins:
                        if message.command[0] == 'biowarn':
                            member = await client.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Dear... {member.user.first_name} "
                                      f"{member.user.last_name if member.user.last_name else ''} "
                                      f"\n[ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly "
                                      f"note that adding links in the bio is not allowed in this group. Let's keep "
                                      f"the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n "
                                      f"#CommunityGuidelines \n\nUpdates : @BlazingSquad")
                            await client.send_message(chat_id, usrtxt)
                        if message.command[0] == 'biomute':
                            await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                            member = await client.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Dear... {member.user.first_name} "
                                      f"{member.user.last_name}\n [ ](tg://user?id={user_id}) \n 🌟 We value your "
                                      f"presence here, but kindly note that adding links in the bio is not allowed in "
                                      f"this group. Let's keep the focus on engaging discussions. Thank you for your "
                                      f"cooperation! 🙌 \n\n #CommunityGuidelines \n\nUpdates : @BlazingSquad")
                            await client.send_message(chat_id, usrtxt)
                        if message.command[0] == 'bioban':
                            await client.ban_chat_member(chat_id, user_id)
                            member = await client.get_chat_member(chat_id, user_id)
                            usrtxt = (f"Regrettably, {member.user.first_name} {member.user.last_name} has faced a ban "
                                      f"due to the inclusion of a link in the bio. 🚫 We clientreciate your "
                                      f"understanding and cooperation in this matter. \n\n #CommunityGuidelines"
                                      f"\n\nUpdates : @BlazingSquad")
                            await client.send_message(chat_id, usrtxt)

                except Exception as e:
                    await message.reply(f"{e} "f"\n\nincorrect, please report :"
                                        f"@BlazingSquad")
                    print(e)
                    return
        except FloodWait as f:
            await asyncio.sleep(f.value)
        except UsernameInvalid:
            return
        except ChannelInvalid:
            return
        except Exception as e:
            print(e)
            await message.reply('I dont have enough permission to do this action ')
            return
        await q.delete()
    else:
        await message.reply('You have to be an admin to do this')
        await q.delete()
        return

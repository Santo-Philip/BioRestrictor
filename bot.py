from pyrogram import Client , filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw import functions, types
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime,timedelta
import re

api_id = 1474940
api_hash = "779e8d2b32ef76d0b7a11fb5f132a6b6"
bot_token = "5804042113:AAH4c4WG0JOuo8S3r9RfnXdjPg89iPdDMug"

app = Client(
        "my_bot",
        api_id = api_id,
        api_hash = api_hash,
        bot_token = bot_token
)


initial_time = datetime.now()
link_pattern = re.compile(r'https:\/\/t.me\/\+\w+|t.me\/\+\w+')
mention_pattern = re.compile(r'@((?!all)[\w\d]+)') 

        
@app.on_message(filters.command(["biowarn","bioban","biomute"]) & filters.group)
async def biocmd(client, message):
        chat_id = message.chat.id
        administrators = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                administrators.append(m.user.id)
        if message.from_user.id in administrators:
                try :
                        async for members in client.get_chat_members(chat_id):
                                user_id = members.user.id
                                userrr = await app.resolve_peer(user_id)
                                try:
                                        ll = await app.invoke(
                                        GetFullUser(
                                                id = userrr
                                                )
                                        )
                                        about =ll.full_user.about
                                        links = link_pattern.findall(about)
                                        plink = mention_pattern.findall(about)
                                        
                                        if plink and user_id not in administrators:
                                              
                                                try:
                                                                r= await app.invoke(
                                                                      functions.channels.GetFullChannel(
                                                                        channel = await app.resolve_peer(plink[0])
                                                                        )
                                                                )
                                                                if r:
                                                                        if message.command[0] == 'biowarn':
                                                                           member = await app.get_chat_member(chat_id, user_id)
                                                                           usrtxt = f"Dear... {member.user.first_name} {member.user.last_name if member.user.last_name else ''}\n [ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly note that adding links in the bio is not allowed in this group. Let's keep the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n #CommunityGuidelines"
                                                                           await app.send_message(chat_id,usrtxt) 
                                                                        if message.command[0] == 'biomute':
                                                                           await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
                                                                           member = await app.get_chat_member(chat_id, user_id)
                                                                           usrtxt = f"Dear... {member.user.first_name} {member.user.last_name} \n[ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly note that adding links in the bio is not allowed in this group. Let's keep the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n #CommunityGuidelines"
                                                                           await app.send_message(chat_id,usrtxt)
                                                                        if message.command[0] == 'bioban':
                                                                           await app.ban_chat_member(chat_id, user_id)
                                                                           member = await app.get_chat_member(chat_id, user_id)
                                                                           usrtxt = f"Regrettably, {member.user.first_name} {member.user.last_name} has faced a ban due to the inclusion of a link in the bio. 🚫 We appreciate your understanding and cooperation in this matter. \n\n #CommunityGuidelines"
                                                                           await app.send_message(chat_id,usrtxt)
                                                               
                                                except BadRequest:
                                                             pass
                                                except Exception:
                                                              pass
                                        if links and user_id not in administrators:
                                                if message.command[0] == 'biowarn':
                                                        member = await app.get_chat_member(chat_id, user_id)
                                                        usrtxt = f"Dear... {member.user.first_name} {member.user.last_name if member.user.last_name else ''} \n[ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly note that adding links in the bio is not allowed in this group. Let's keep the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n #CommunityGuidelines"
                                                        await app.send_message(chat_id,usrtxt) 
                                                if message.command[0] == 'biomute':
                                                        await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
                                                        member = await app.get_chat_member(chat_id, user_id)
                                                        usrtxt = f"Dear... {member.user.first_name} {member.user.last_name}\n [ ](tg://user?id={user_id}) \n 🌟 We value your presence here, but kindly note that adding links in the bio is not allowed in this group. Let's keep the focus on engaging discussions. Thank you for your cooperation! 🙌 \n\n #CommunityGuidelines"
                                                        await app.send_message(chat_id,usrtxt)
                                                if message.command[0] == 'bioban':
                                                        await app.ban_chat_member(chat_id, user_id)
                                                        member = await app.get_chat_member(chat_id, user_id)
                                                        usrtxt = f"Regrettably, {member.user.first_name} {member.user.last_name} has faced a ban due to the inclusion of a link in the bio. 🚫 We appreciate your understanding and cooperation in this matter. \n\n #CommunityGuidelines"
                                                        await app.send_message(chat_id,usrtxt)
                                       
                                except Exception as e:
                                   print(e)
                except Exception as e :
                        print(e)
                        await message.reply('I dont have enough permission to do this action ')
        else:
                await message.reply('You have to be an admin to do this')
 
@app.on_message(filters.command("start"))
async def start(client, message):
        button = InlineKeyboardButton("Join our channel", url="https://t.me/BlazingSquad")
        keyboard = InlineKeyboardMarkup([[button]])
        startstr = "🌟 Greetings! I am a modern Telegram bot here to assist you in maintaining a link-free environment.\n\n 🚨 Use /biowarn to elegantly warn users about their bio content. \n\n 🔨 Employ /bioban to gracefully ban users who persistently include links in their bios. \n\n🔇 Enhance order with /biomute to tactfully mute users. \n\n Let's keep the community thriving! \n\n 🤖 @BlazingSquad"
        await message.reply(text=startstr, reply_markup=keyboard)
                
@app.on_message(filters.group & ~filters.left_chat_member)
async def msg_check(client,message):
        time = initial_time + timedelta(hours=int(5))
        user_id = message.from_user.id
        first = message.from_user.first_name
        last = message.from_user.last_name
        chat_id = message.chat.id
        administrators = []
        menid = []
        menid.append(user_id)
        mentions = f"Dear... {first} {last if last else ''}\n🌟 Your profile has been flagged to administrators 🚩 due to the presence of a link in your bio. \n\n🎋 Please remove it before taking any actions\n\n ID : `{user_id}`"
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                menid.append(m.user.id)
                administrators.append(m.user.id)
        for id in menid:
               mentions += f"[\u2063](tg://user?id={id})"
        try:
                user = await app.resolve_peer(user_id)
                try:
                        user_detail= await app.invoke(GetFullUser(id=user))
                        about = user_detail.full_user.about
                        links = link_pattern.findall(about)
                        plink = mention_pattern.findall(about)
                        if plink and user_id not in administrators:
                                await message.delete()
                                await app.invoke(functions.channels.GetFullChannel( channel = await app.resolve_peer(plink[0])))
                                try:
                                         await app.restrict_chat_member(chat_id, user_id, ChatPermissions(),time)
                                except Exception as e:
                                        print(e)
                                 
                                await app.send_message(chat_id,mentions)
                        if links and user_id not in administrators:
                                 await message.delete()
                                 try:
                                         await app.restrict_chat_member(chat_id, user_id, ChatPermissions(),time)
                                 except Exception as e:
                                        print(e)
                                 await app.send_message(chat_id,mentions) 
                except Exception as e:
                        print(e)
        except Exception as e:
                print(e)

try:
        app.run()
except KeyboardInterrupt:
        app.stop()
from config import LOG,OWNER
from utils.mongo import Database
from pyrogram.errors import FloodWait,UserIsBlocked, InputUserDeactivated, PeerIdInvalid
import asyncio
from pyrogram import Client,filters

@Client.on_message(filters.command('br') & filters.user(OWNER),group=13)
async def broadcast(bot,msg):
  if len(msg.command) > 1:
    data = Database.fetchall('biobot')
    success = []
    failed = []
    for value in data:
      try:
        await bot.send_message(chat_id=value['user'],text=msg.command[1])
        success.append(value['user'])
      except UserIsBlocked :
        failed.append(value['user'])
      except InputUserDeactivated :
        failed.append(value['user'])
      except PeerIdInvalid:
        failed.append(value['user'])
      except FloodWait as f:
        await asyncio.sleep(f.value)
      except Exception as e:
        await bot.send_message(chat_id=LOG,text=f"Error Occured : \n\n User : {value['user']} \n\nError : {e}")
        failed.append(value['user'])
    await msg.reply(f"Broadcast for users Completed\n\nSuccess : {len(success)} Users\n\nFailed : {len(failed)} users")
  else :
    data = Database.fetchall('biobot')
    success = []
    failed = []
    for value in data:
      try:
        await msg.reply_to_message.copy(value['user'])
        success.append(value['user'])
      except UserIsBlocked :
        failed.append(value['user'])
      except InputUserDeactivated :
        failed.append(value['user'])
      except PeerIdInvalid:
        failed.append(value['user'])
      except FloodWait as f:
        await asyncio.sleep(f.value)
      except Exception as e:
        await bot.send_message(chat_id=LOG,text=f"Error Occured : \n\n User : {value['user']} \n\nError : {e}")
        failed.append(value['user'])
    await msg.reply(f"**Broadcast for users** Completed\n\nSuccess : **{len(success)} Users**\n__Failed : {len(failed)} users__")
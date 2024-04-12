import asyncio
import diskcache as dc
from pyrogram import enums
from functools import lru_cache

chat_admins = []
cache = dc.Cache("/cache")


async def get_admins(app, msg):
    chat_id = msg.chat.id
    admins = cache.get(chat_id)
    if admins is None:
        admins = []
        cache.set(chat_id, admins)
    async for m in app.get_chat_members(chat_id=chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(m.user.id)
    cache.set(chat_id, admins)


async def add_group(chat):
    groups = cache.get('groups')
    if groups is None:
        groups = [chat]
    else:
        groups.append(chat)
    cache.set('groups', groups)

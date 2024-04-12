import asyncio
import diskcache as dc
from pyrogram import enums

cache = dc.Cache("/cache")


async def period_check(client):
    while True:
        chat_ids = cache.get('groups')
        if chat_ids is not None:
            for chat_id in chat_ids:
                new_admins = []
                async for m in client.get_chat_members(chat_id=chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    new_admins.append(m.user.id)

                cached_admins = cache.get(chat_id, [])
                admins_to_remove = [admin for admin in cached_admins if admin not in new_admins]

                # Remove admins who are no longer administrators
                for admin_to_remove in admins_to_remove:
                    cached_admins.remove(admin_to_remove)

                # Add new admins
                for new_admin in new_admins:
                    if new_admin not in cached_admins:
                        cached_admins.append(new_admin)

                cache.set(chat_id, cached_admins)
                await asyncio.sleep(10)

            await asyncio.sleep(5)
        else:
            await asyncio.sleep(5)

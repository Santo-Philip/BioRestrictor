from pyrogram import Client, filters, enums
import diskcache as dc

cache = dc.Cache("/cache")
@Client.on_message(filters.command('reload'))
async def reload(bot, msg):
    chat = msg.chat.id
    groups = cache.get('groups', [])  # Fetch groups or initialize an empty list if not present
    if chat not in groups:
        groups.append(chat)
        cache.set('groups', groups)

    try:
            new_admins = []
            async for member in bot.get_chat_members(chat_id=chat, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                new_admins.append(member.user.id)

            cached_admins = cache.get(chat, [])
            admins_to_remove = [admin for admin in cached_admins if admin not in new_admins]
            for admin_to_remove in admins_to_remove:
                cached_admins.remove(admin_to_remove)

            for new_admin in new_admins:
                if new_admin not in cached_admins:
                    cached_admins.append(new_admin)

            cache.set(chat, cached_admins)
            print(f"Reloaded admins for chat {chat}")
            msg.reply('Reloaded admins')
    except Exception as e:
            print(f"Error reloading admins for chat {chat}: {e}")
            msg.reply(f"Error reloading admins : {e}\n\nReport : @BlazingSquad")

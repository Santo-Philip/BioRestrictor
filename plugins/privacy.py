from pyrogram import Client,filters

@Client.on_message(filters.command('privacy')& filters.private)
async def privacy(msg,bot):
  await msg.reply("Privacy Policy for BioRestrictorBot\n\n1. **Introduction** BioRestrictorBot is a Telegram bot designed to restrict users who have links in their bios.\n2. **Data Collection** We collect the following data from users:Usernames User IDs Bio text This data is collected via Telegram's API when users interact with the bot.\n3. **Data Usage** The collected data is used solely to check for links in user bios and to restrict users if links are found.\n4. **Temporary Data Storage** Certain data may be stored temporarily in memory for processing purposes. This data is not stored permanently. Temporary storage duration is kept to a minimum necessary to fulfill the bot's functionality.\n5. **Data Storage Data** is stored securely on our servers and is retained for as long as necessary to fulfill the bot's purpose. We implement industry-standard security measures to protect your data.\n6. **Data Sharing** We do not share your data with third parties, except as required by law. Your data will not be sold or used for marketing purposes.\n7. **Policy Changes** We may update this privacy policy from time to time. Any changes will be posted on this page, and the date of the latest update will be indicated at the top.\n8. **Contact Information** If you have any questions or concerns about this privacy policy, please contact us @BlazingSquad.\n9. **Compliance We comply** with all relevant data protection regulations, including the GDPR.")
import asyncio
from telethon import TelegramClient, events
from telegram import Bot

# Your Telegram API credentials (from https://my.telegram.org)
API_ID = 26512850  # integer, e.g., 1234567
API_HASH = 'a51477d8c5205718ddec7dd922f36e57'  # string, e.g., 'abcdef1234567890abcdef1234567890'

# Telegram bot token to forward messages to
BOT_TOKEN = '7638002415:AAFaMZfmi08ylMP2siKm_YvPme0MEbFty38'

# Telegram chat ID where bot will send forwarded messages
# Usually your own chat ID with the bot; you can get it from @userinfobot or from updates
BOT_CHAT_ID = YOUR_TELEGRAM_USER_ID  # integer, e.g., 123456789

# Initialize Telethon client (user client)
client = TelegramClient('session_name', API_ID, API_HASH)

# Initialize Telegram Bot API
bot = Bot(token=BOT_TOKEN)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Only handle private chats (DMs)
    if event.is_private:
        sender = await event.get_sender()
        sender_name = sender.first_name if sender else "Unknown"
        message_text = event.raw_text
        
        forward_text = f"New DM from {sender_name}:\n\n{message_text}"
        
        # Send message to bot chat
        await bot.send_message(chat_id=BOT_CHAT_ID, text=forward_text)

async def main():
    print("Starting Telegram client...")
    await client.start()
    print("Client started. Listening for new DMs...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())

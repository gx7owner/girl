import os
import random
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Replace with your actual bot tokens from BotFather
TOKENS = [
    'BOT_TOKEN_1',
    'BOT_TOKEN_2',
    'BOT_TOKEN_3'
]

TEXT_FILE = 'text.txt'
PHOTO_DIR = 'photos'

# Make sure photos directory exists
os.makedirs(PHOTO_DIR, exist_ok=True)

# Store last user_id per bot username to send messages/photos
user_ids = {}

def load_messages():
    """Load messages from text.txt file, one sentence per line."""
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines
    return []

async def save_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save photo sent by user to PHOTO_DIR folder."""
    user_id = update.effective_chat.id
    bot_name = context.bot.username
    user_ids[bot_name] = user_id

    photo = update.message.photo[-1]  # Get highest quality photo
    file = await photo.get_file()
    filename = f"{bot_name}_{file.file_id}.jpg"
    file_path = os.path.join(PHOTO_DIR, filename)

    await file.download_to_drive(file_path)
    await update.message.reply_text("Photo saved baby!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user_id = update.effective_chat.id
    bot_name = context.bot.username
    user_ids[bot_name] = user_id
    await update.message.reply_text("Hey jaan, main ready hoon tumhare liye!")

async def auto_sender(app, bot_name):
    """Send random text and photo every 10 seconds to last active user."""
    bot = app.bot
    while True:
        user_id = user_ids.get(bot_name)
        if user_id:
            messages = load_messages()
            if messages:
                msg = random.choice(messages)
                await bot.send_message(chat_id=user_id, text=msg)

            photos = [f for f in os.listdir(PHOTO_DIR) if f.endswith('.jpg')]
            if photos:
                photo_path = os.path.join(PHOTO_DIR, random.choice(photos))
                with open(photo_path, 'rb') as photo:
                    await bot.send_photo(chat_id=user_id, photo=photo)
        await asyncio.sleep(10)

async def run_bots():
    apps = []

    for token in TOKENS:
        app = ApplicationBuilder().token(token).build()
        await app.initialize()
        bot_name = (await app.bot.get_me()).username

        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.PHOTO, save_photo))

        await app.start()
        apps.append(app)

        # Start sending messages/photos every 10 seconds
        asyncio.create_task(auto_sender(app, bot_name))

    # Keep all bots running
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_bots())

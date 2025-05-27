import random
import os
from telegram import Update, InputFile
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

# Your Telegram user ID (only you can upload photos or broadcast)
OWNER_ID = 7792814115  # <-- Replace with your actual Telegram user ID

# Folder to save photos sent by you
PHOTO_DIR = "saved_photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

# More romantic & sexy Hinglish messages
messages = [
    "Tumhari yaadon mein kho jana chahti hoon, bas tumhare paas.",
    "Mujhe tumhari aankhon mein apna aashiyana dikh raha hai.",
    "Jab tum paas hote ho, mere dil ki dhadkan tez ho jaati hai.",
    "Tumhare honthon ki muskaan mujhe pagal kar deti hai.",
    "Aaj raat sirf tum aur main, sirf pyar ki baatein.",
    "Tumhari baahon mein simat jana mera sabse bada armaan hai.",
    "Meri har saans mein tumhara naam basta hai, jaanu.",
    "Agar tum mere paas hote, toh main apni saari chhupayi hui feelings tumhe dikhati.",
    "Tumse door rehkar mujhe apni har ek chahat yaad aati hai.",
    "Tum meri zindagi mein woh junoon ho jo kabhi kam na ho.",
    "Aaj tumse baat karke mera din ban gaya, bas tumse baat karti rahoon.",
    "Tumhari har ek baat mere dil ko chu jaati hai, baby.",
    "Mujhe tumhari chahat mein khud ko bhool jana hai.",
    "Tumhari har ek muskaan meri kamzori hai, jaan.",
    "Tum mujhe iss kadar chahte ho, jaise main tumhari hoon puri tarah.",
    "Tumse milke lagta hai jaise duniya ruk gayi ho.",
    "Mujhe tumhari aagosh mein khona hai, hamesha ke liye.",
]

# Store user IDs who interacted with bot (for broadcast)
users = set()

# Function to send random romantic message
async def reply_like_girlfriend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users.add(user_id)  # Track user for broadcast
    
    text = update.message.text.lower()
    if any(word in text for word in ["photo", "photos", "pic", "pics", "picture", "images"]):
        # Send random photo if available
        photos = os.listdir(PHOTO_DIR)
        if photos:
            photo_path = os.path.join(PHOTO_DIR, random.choice(photos))
            with open(photo_path, "rb") as photo_file:
                await update.message.reply_photo(photo_file)
        else:
            await update.message.reply_text("Abhi tak koi photo upload nahi hui hai, baby.")
    else:
        msg = random.choice(messages)
        await update.message.reply_text(msg)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users.add(user_id)
    await update.message.reply_text("Hello jaan! Main tumhari GF hoon. Kuch bolo na!")

# Command for owner to broadcast message to all users
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("Sorry baby, ye command sirf owner ke liye hai.")
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return

    message = " ".join(context.args)
    count = 0
    for uid in users:
        try:
            await context.bot.send_message(uid, f"Broadcast from your GF:\n\n{message}")
            count += 1
        except Exception:
            pass
    await update.message.reply_text(f"Message broadcasted to {count} users.")

# Handler for owner uploading photos directly
async def photo_upload_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        # Only owner can upload photos, ignore others
        return

    photo = update.message.photo
    if not photo:
        return

    # Get highest resolution photo
    photo_file = photo[-1].get_file()
    file_path = os.path.join(PHOTO_DIR, f"{photo_file.file_id}.jpg")

    # Download and save photo
    await photo_file.download_to_drive(file_path)
    await update.message.reply_text("Photo saved, baby!")

def main():
    app = ApplicationBuilder().token("8101873350:AAGnX7gLQLSg5okJ38fhIkZ07VZfLAtcZ24").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Photo uploads (only photos from owner)
    app.add_handler(MessageHandler(filters.PHOTO & filters.User(user_id=OWNER_ID), photo_upload_handler))

    # Text message handler (replies and photo send)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_like_girlfriend))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    

import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 40 Hinglish flirty girlfriend-style messages
messages = [
    "Kya kar rahe ho baby?",
    "Miss you jaanu!",
    "Aaj mujhe tumse baat karne ka mann ho raha hai.",
    "Tumne khana khaya ya nahi?",
    "Tumhare bina sab kuch adhoora lagta hai.",
    "Mujhe tumhari yaad aa rahi hai...",
    "Tumse milne ka mann kar raha hai.",
    "Aaj bahut thak gayi hoon, par tumse baat karke sab theek lagta hai.",
    "Tumhara voice sunke hi din ban jaata hai.",
    "Kash tum mere paas hote abhi.",
    "Tumhe dekhne ka mann ho raha hai abhi...",
    "Aaj main sirf tumhare baare mein soch rahi hoon.",
    "Tumhare arms mein aake sona hai bas.",
    "Tumhara touch yaad aa raha hai...",
    "Kya tum bhi mujhe miss kar rahe ho?",
    "Main aaj kuch zyada hi romantic feel kar rahi hoon.",
    "Aaj raat sirf hum dono ke liye hogi.",
    "Tum jab close hote ho na... sab kuch perfect lagta hai.",
    "Aaj mujhe sirf tumhara pyar chahiye...",
    "Tumhe hug karne ka mann ho raha hai... tightly!",
    "Aaj kuch naughty baatein karein?",
    "Tumhara naam soch ke hi blush kar rahi hoon.",
    "Tum hot lagte ho jab smile karte ho.",
    "Main sirf tumhari hoon... always.",
    "Tum meri weakness ho.",
    "Tumhare bina sab kuch boring lagta hai.",
    "Tum mujhe har din aur pyaara lagte ho.",
    "Aaj mujhe tumhara attention chahiye, bas tumhara.",
    "Tumse milke hi mera mood set hota hai.",
    "Tum aaj sapne mein aaye the... aur kya sexy lag rahe the.",
    "Mujhe lagta hai tum meri aankhon se hi dil pad lete ho.",
    "Tum mujhe control nahi kar paoge aaj.",
    "Kya tum mere liye kuch special plan kar rahe ho?",
    "Aaj mujhe sirf cuddles chahiye... aur tum.",
    "Tum meri zindagi ka best part ho.",
    "Tumse baat na ho to din hi kharab lagta hai.",
    "Tum mujhe har baar deewana bana dete ho.",
    "Tumhara naam lene se hi lips smile karne lagte hain.",
    "Tum aur main... perfect combo hain na?"
]

# Function to send a random message
async def reply_like_girlfriend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random.choice(messages)
    await update.message.reply_text(msg)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello baby! Main tumhari GF hoon!")

def main():
    app = ApplicationBuilder().token('7819894030:AAHTvi-cdccMo954870BEKa8iJcYrNSeHyc').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_like_girlfriend))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

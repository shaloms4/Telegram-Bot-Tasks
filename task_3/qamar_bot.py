import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Define a function for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am Qamar, your moon bot 🌙.')

# Create an Application instance 
application = Application.builder().token(TOKEN).build()

# Add the handler for the /start command
application.add_handler(CommandHandler('start', start))

# Start the bot
application.run_polling()

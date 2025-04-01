import logging
import os
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
load_dotenv()  

TOKEN = os.getenv('TELEGRAM_TOKEN')
print(f"Token loaded: {TOKEN}") 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Qamar Bot...')

# Command Handlers
async def start_command(update: Update, context):
    await update.message.reply_text('🌙 Hello! I\'m Qamar, your guide to the moon! Type /help to learn more.')

async def help_command(update: Update, context):
    await update.message.reply_text('I can help you learn about the moon! Try typing /about or ask me any moon-related question.')

async def about_command(update: Update, context):
    await update.message.reply_text('Qamar means "moon" in Arabic. I can teach you about moon phases, facts, and more!')

# Message Handler 
async def handle_message(update: Update, context):
    text = str(update.message.text).lower()  
    
    if re.search(r'\bmoon\b', text): 
        response = "🌕 The moon has four phases: New Moon, First Quarter, Full Moon, and Last Quarter."
        await update.message.reply_text(response)
    else:
        response = "I can help you learn more about the moon! Just mention it."
        await update.message.reply_text(response)

# Error handler
async def error(update: Update, context):
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('about', about_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_error_handler(error)

    application.run_polling()

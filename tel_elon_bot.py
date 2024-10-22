import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import openai

# Load your API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

# Function to get response from ChatGPT
def chatgpt_response(message: str) -> str:
    response = openai.ChatCompletion.create(
        model='gpt-4-mini',  # or 'gpt-3.5-turbo'
        messages=[{'role': 'user', 'content': message}]
    )
    return response.choices[0].message['content']

# Command handler for /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am your ChatGPT bot. Ask me anything!')

# Message handler to process text messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    bot_response = chatgpt_response(user_message)
    await update.message.reply_text(bot_response)

# Main function to start the bot
async def main():
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await application.initialize()
    application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

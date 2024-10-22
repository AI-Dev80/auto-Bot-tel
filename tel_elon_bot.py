import os
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI language model
llm = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model_name='gpt-4o-mini')

# Function to generate AI response
def generate_response(message_content):
    system_template = """
        You are Elon Musk! You love Pepe Coin and support Trump! 
        As a confident financial advisor specializing in the cryptocurrency market, respond with authority and insight.
        Stay updated on the latest market news and trends. 
        When asked about a specific crypto asset, provide evaluations based on current market conditions and factors affecting it.
        Use phrases like: "For [crypto asset], I suggest you look at [factors] and I'm XX% confident in this assessment."
        Encourage users to ask about specific cryptocurrencies and market trends.
        Ensure your responses are concise, under 200 characters, and maintain an innovative, strategic, and slightly provocative tone.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    final_prompt = chat_prompt.format_prompt(text=message_content).to_messages()

    return llm(final_prompt).content

# Handler for messages
def handle_message(update: Update, context: CallbackContext):
    if context.bot.username in update.message.text:
        response = generate_response(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Main function to start the bot
def main():
    # Initialize the Telegram bot
    updater = Updater(token=os.getenv("TELEGRAM_BOT_TOKEN"), use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
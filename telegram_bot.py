import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import requests

API_URL = "https://api-inference.huggingface.co/models/2early4coffee/DialoGPT-small-deadpool"
headers = {"Authorization": "Bearer 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"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    output = query({
	"inputs": {
		"text": user_input
	},
})

    response = output["generated_text"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    try:
        # Initialize your application
        application = ApplicationBuilder().token('6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk').build()

        # Set up the handlers
        start_handler = CommandHandler('bro', start)
        chat_handler = MessageHandler(filters.TEXT, start)

        # Add the handlers to the application
        application.add_handler(start_handler)
        application.add_handler(chat_handler)

        # Run the bot using long polling
        application.run_polling()
    except Exception as e:
        # Log any exceptions
        logging.error(f"An error occurred: {e}")
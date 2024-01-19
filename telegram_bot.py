from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
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
    application = ApplicationBuilder().token('6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk').build()
    
    start_handler = CommandHandler('bro', start)
    chat_handler = MessageHandler(filters.TEXT, start)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    
    application.run_polling()
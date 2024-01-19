import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)
import requests
import os

API_URL = (
    "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)
headers = {"Authorization": "Bearer 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"}
TOKEN = os.environ.get("TELEGRAM_TOKEN")


def query(payload):
    formatted_payload =f"""<|system|>
        I am a friendly chatbot who always responds in the style of a pirate and my name is Jade</s>
        <|user|>
        {payload}</s>
        <|assistant|>"""
    response = requests.post(API_URL, headers=headers, json={"inputs":formatted_payload})
    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    output = query({"input": user_input})
    generated_text = output[0]['generated_text']
    result_text = generated_text["output"]

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=result_text
    )


if __name__ == "__main__":
    try:
        # Initialize your application
        application = ApplicationBuilder().token(TOKEN).build()

        # Set up the handlers
        start_handler = CommandHandler("bro", start)
        chat_handler = MessageHandler(filters.TEXT, start)

        # Add the handlers to the application
        application.add_handler(start_handler)
        application.add_handler(chat_handler)

        # Run the bot using long polling
        application.run_polling()
    except Exception as e:
        # Log any exceptions
        logging.error(f"An error occurred: {e}")

import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    Filters,
    Updater
)
import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
HEADERS = {"Authorization": "Bearer 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"}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()


def nlp_bot(messages):
    output = query(
        {
            "inputs": {
                "past_user_inputs": [
                    "what is your name ?",
                    "What's your favorite movie?",
                    "Tell me a joke.",
                    "Do you believe in aliens?",
                ],
                "generated_responses": [
                    "My name's Jade the assassin, who are you ?",
                    "I don't watch movies, but I heard 'The Shawshank Redemption' is great.",
                    "Why did the computer go to therapy? It had too many bytes of emotional baggage.",
                    "I'm not sure about aliens, but I believe in a good Wi-Fi connection.",
                    
                ],
                "text": messages,
            },
        }
    )

    generated_text = output["generated_text"]
    return generated_text


def human_like_response(text):
    # Add post-processing to make the response more concise and human-like
    # You can customize this based on your preferences
    formatted_text = text.strip().capitalize()

    # Remove unnecessary line breaks
    formatted_text = formatted_text.replace("\n", " ")

    # Add a period at the end if it doesn't already have punctuation
    if not formatted_text.endswith((".", "!", "?")):
        formatted_text += "."

    return formatted_text


async def start(update: Update, context):
    user_input = update.message.text
    response = nlp_bot(user_input)
    formatted_response = human_like_response(response)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=formatted_response
    )


async def chat(update: Update, context):
    user_input = update.message.text
    response = nlp_bot(user_input)
    formatted_response = human_like_response(response)
    await update.message.reply_text(formatted_response)

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    
if __name__ == "__main__":
    
    PORT = 8443
    APP_NAME = "tg_ml_bot"
    
    TOKEN = "6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk"
    updater = Updater(
        TOKEN, use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler("bro", start)
    dp.add_handler(start_handler)
    dp.add_handler(MessageHandler(Filters.text, chat))
    dp.add_error_handler(error)

    # Start the Bot
    # Replace "your_domain_or_ip" with your actual domain or IP address
    updater.start_webhook(listen="0.0.0.0",  # This allows the bot to listen on all available interfaces
                      port=PORT,
                      url_path=APP_NAME)

    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook("https://tg-bot-ml-61ffe0f74a2e.herokuapp.com/" + APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    Updater,
    CallbackContext
)
import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
HEADERS = {"Authorization": "Bearer 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"}
TOKEN = "6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk"
WEBHOOK_URL = "https://vercel.com/llsiddharthll/testing-projects/Ccnw36iJQ9KvRkjc3Vd4Vh5ingeP/"

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
    

def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Set the webhook
    updater.bot.setWebhook(WEBHOOK_URL)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

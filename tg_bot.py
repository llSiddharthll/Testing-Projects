import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
import requests

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
HEADERS = {"Authorization": "Bearer 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"}


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = nlp_bot(user_input)
    formatted_response = human_like_response(response)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=formatted_response
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = nlp_bot(user_input)
    formatted_response = human_like_response(response)
    await update.message.reply_text(formatted_response)


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk")
        .build()
    )

    start_handler = CommandHandler("bro", start)
    chat_handler = MessageHandler(filters.TEXT, chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    application.run_polling()

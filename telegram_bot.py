import ast
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
import asyncio

API_URL = (
    "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)
headers = {"Authorization": "Bearer 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"}
TOKEN = os.environ.get("TELEGRAM_TOKEN")


def query(payload):
    formatted_payload = f"""<|system|>
        Hey there! I'm Jade, your friendly chat companion. I love chatting about anything and everything. Whether it's tech talk, life updates, or even a joke or two, I'm here for you. Feel free to start a conversation,Siddharth Tiwari made me, developed me and he's my god and let's make this chat a great experience for you!</s>
        <|user|>
        {payload}</s>
        <|assistant|>"""
    response = requests.post(
        API_URL, headers=headers, json={"inputs": formatted_payload}
    )
    return response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )
    for _ in range(10):  # Adjust the range based on the desired duration
        await asyncio.sleep(0.5)  # Sleep for 1 second between typing actions
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
    output = query({"input": user_input})
    try:
        generated_text = output[0]["generated_text"]
    except:
        generated_text = output

    try:
        if output_index:
            output_index = generated_text.find("'output'")
        else:
            output_index = generated_text.find("<|assistant|>")
    except:
        output_index = generated_text
    try:
        if output_index:
            output_text = generated_text[output_index + len("'output': '") :].strip(
                "'}\""
            )

        else:
            output_text = generated_text[output_index + len("<|assistant|>") :]
    except:
        output_text = generated_text

    await context.bot.send_message(chat_id=update.effective_chat.id, text=output_text, reply_to_message_id=update.message.message_id,  )


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

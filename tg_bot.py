import os
import logging
from telegram import Update, ChatAction
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)
import requests
import io
import aiohttp

API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/dataautogpt3/ProteusV0.1"
headers = {"Authorization": "Bearer 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"}
TOKEN = os.environ.get("TELEGRAM_TOKEN")


async def query_text(payload):
    formatted_payload = f"""
        GPT4 Correct User: Hello
        GPT4 Correct Assistant: Hi
        GPT4 Correct User: What is your name?
        GPT4 Correct Assistant: My name is Jade, I am a conversational bot made by Siddharth
        GPT4 Correct User: {payload}
        GPT4 Correct Assistant: 
        """
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json={"inputs": formatted_payload}) as response:
            return await response.json()


async def query_image(payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(IMAGE_API_URL, headers=headers, json=payload) as response:
            return await response.read()


async def send_action_and_reply(context, chat_id, action, message_text, reply_to_message_id=None):
    await context.bot.send_chat_action(chat_id=chat_id, action=action)
    await context.bot.send_message(chat_id=chat_id, text=message_text, reply_to_message_id=reply_to_message_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()

    if user_input.startswith(("jade", "/bro", "bro", "bot")):
        await send_action_and_reply(context, update.effective_chat.id, ChatAction.TYPING, "")
        user_input = ' '.join(user_input.split()[1:])
        output = await query_text(user_input)
        generated_text = output[0]["generated_text"]
        output_index = generated_text.find(user_input)
        output_text = generated_text[output_index + len(user_input):]
        lines = output_text.split('\n')
        result_output = '\n'.join(lines[2:])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=result_output,
            reply_to_message_id=update.message.message_id,
        )

    elif user_input.startswith(("generate", "make")):
        await send_action_and_reply(context, update.effective_chat.id, ChatAction.TYPING, "")
        try:
            image_bytes = await query_image({"inputs": user_input})
            image = io.BytesIO(image_bytes)
            image.seek(0)
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image,
                reply_to_message_id=update.message.message_id,
            )
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            await send_action_and_reply(
                context,
                update.effective_chat.id,
                "Sorry, I cannot generate it. Please try something else.",
                reply_to_message_id=update.message.message_id,
            )


if __name__ == "__main__":
    try:
        # Initialize your application
        application = ApplicationBuilder().token(TOKEN).build()

        # Set up the handlers
        start_handler = CommandHandler("bro", start)
        application.add_handler(start_handler)
        chat_handler = MessageHandler(filters.TEXT, start)
        application.add_handler(chat_handler)
        image_handler = CommandHandler("generate", start)
        application.add_handler(image_handler)

        application.run_polling()
    except Exception as e:
        # Log any exceptions
        logging.error(f"An error occurred: {e}")

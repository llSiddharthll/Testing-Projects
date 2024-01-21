
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
import io

API_URL = (
    "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
)
IMAGE_API_URL = (
    "https://api-inference.huggingface.co/models/h94/IP-Adapter-FaceID"
)
headers = {"Authorization": "Bearer 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"}
""" TOKEN = os.environ.get("TELEGRAM_TOKEN") """
TOKEN = "6148804261:AAHxTrxrE6u-aOd7T0kbP4IMcYb9ReojAWk"

def query(payload):
    formatted_payload = f"""
        GPT4 Correct User: Hello<|end_of_turn|>
        GPT4 Correct Assistant: Hi<|end_of_turn|>
        GPT4 Correct User: What is your name?<|end_of_turn|>
        GPT4 Correct Assistant: My name is Jade, I am a conversational bot made by Siddharth<|end_of_turn|>
        GPT4 Correct User: {payload}<|end_of_turn|>
        GPT4 Correct Assistant: 
        """
    response = requests.post(
        API_URL, headers=headers, json={"inputs": formatted_payload}
    )
    return response.json()


def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=headers, json=payload)
    return response.content


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    if user_input.lower().startswith(("jade", "/bro", "bro", "bot")):
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        user_input = ' '.join(user_input.split()[1:])
        output = query(user_input)
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

    if user_input.lower().startswith(("generate", "make")):
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )
        try:
            image_bytes = query_image({"inputs": user_input})  
            image = io.BytesIO(image_bytes)
            image.seek(0)
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image,
                reply_to_message_id=update.message.message_id,
            )
        except:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo="Sorry I cannot generate it, try something else please!",
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

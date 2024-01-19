import discord
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": "Bearer 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"}

TOKEN = os.environ.get('DISCORD_TOKEN')

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content:
            user_input = message.content
            output = query({
                "inputs": {
                    "text": user_input
                },
            })
            await message.channel.send(output["generated_text"])

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
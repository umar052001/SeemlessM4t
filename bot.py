import discord
from discord.ext import commands
from gradio_client import Client
import requests
# Initialize the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize the Gradio client
gradio_client = Client("https://facebook-seamless-m4t.hf.space/")

# Your Discord webhook URL
webhook_url = 'your_weburl'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
@bot.command()
async def translate(ctx, source_lang, target_lang, *, text):
    result = gradio_client.predict(
        "T2TT (Text to Text translation)",
        "text",
        text,
        source_lang,
        target_lang,
        api_name="/run"
    )

    translated_text = result[0]['output']

    await ctx.send(f'Translated ({target_lang}): {translated_text}')

    # Send the translated text to the Discord webhook
    webhook_payload = {'content': f'Translated ({target_lang}): {translated_text}'}
    response = requests.post(webhook_url, json=webhook_payload)

    if response.status_code == 204:
        print("Webhook message sent successfully")
    else:
        print(f"Failed to send message to the webhook. Status code: {response.status_code}")

bot.run('Your_token')

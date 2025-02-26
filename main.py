import discord
import os
from dotenv import load_dotenv

#load the environment variables
load_dotenv()

#------------------------------------------------------------------------------------------------

#discord intents
intents = discord.Intents.default()
intents.messages_content = True

# Create a new Discord client
client = discord.Client(intents=intents)

#------------------------------------------------------------------------------------------------


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


# Get the token value from environment variable
token = os.getenv('TOKEN')
if token is None:
    raise ValueError("TOKEN environment variable is not set or .env file not found")

client.run(token)  # Discord Bot Token 
import discord
import os
from dotenv import load_dotenv
import requests
import json

#load the environment variables
load_dotenv()

#------------------------------------------------------------------------------------------------
""" 
Creates a new Discord client and sets the intents.
These intents are used to specify which events the bot will receive, they must correspond to the 
permissions the bot has in the server, as set in the developer portal.

## TODO: Work out how to manage if a user changes the bots permissions within the server.
-> Check the persssions and change to match the intents?
-> use swithc or if cases?
-> use a template style system to set the permissions?
-> use a config file to set the permissions?
-> dont allow the user to change the permissions?
"""

#discord intents
intents = discord.Intents.default()
intents.message_content = True
# Create a new Discord client
client = discord.Client(intents=intents)

#------------------------------------------------------------------------------------------------


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    print (json_data)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    print (quote)
    return quote



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)


# Get the token value from environment variable
token = os.getenv('TOKEN')
if token is None:
    raise ValueError("TOKEN environment variable is not set or .env file not found")

client.run(token)  # Discord Bot Token 
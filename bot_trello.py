import discord
from trello import TrelloClient
from dotenv import dotenv_values

config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True



trello_client = TrelloClient(
        api_key=config["API_KEY"],
        api_secret=config["API_SECRET"],
        token=config["TOKEN"]
        )

client = discord.Client(intents=intents)


def check_if_good_format(message):
    exploded_msg = (message.content).split(" ")
    if len(exploded_msg) >= 3:
        boards = exploded_msg[1]
        #"..." check if the boards exists
        cards_to_add = exploded_msg[2:]
        return boards, cards_to_add
    return None, None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello :)")
    if message.content.startswith("/add_card"):
        boards, cards = check_if_good_format(message)
        if (boards and cards):
            await message.channel.send("Added in {}: {}".format(boards, cards))
        else:
            await message.channel.send("Nope, your command must looking like this: /add_card [boards] [cards]")


client.run(config["BOT_TOKEN"])

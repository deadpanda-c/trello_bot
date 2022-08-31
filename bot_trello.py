import discord
import trello
from dotenv import dotenv_values

BOARD_ID = None
config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True

trello_client = trello.TrelloClient(
        api_key=config["API_KEY"],
        api_secret=config["API_SECRET"],
        token=config["TOKEN"]
        )

client = discord.Client(intents=intents)

def getBoard():
    all_boards = trello_client.list_boards()
    for board in all_boards:
        if board.name == config["CURRENT_BOARD"]:
            if not board.closed:
                return board.id

def check_inside_boards(all_boards):
    for board in all_boards:
        if board.name == config["CURRENT_BOARD"]:
            if not board.closed:
                BOARD_ID = board.id
                all_lists = trello_client.get_board(BOARD_ID).all_lists()
                return 0, all_lists
    return -1, None

async def find_list(all_lists, name_of_list, message):
    for final_list in all_lists:
        if final_list.name == name_of_list:
            return final_list
    await message.channel.send("This list doesn't exist, if you want to create it, use /add_list")


async def add_card(message):
    exploded_msg = (message.content).split(" ")
    if len(exploded_msg) >= 3:
        list_name = exploded_msg[1]
        name_of_card = exploded_msg[2:].replace('"', '')
        all_boards = trello_client.list_boards()
        status, all_lists = check_inside_boards(all_boards)
        if status == 0 and all_lists:
            list_to_complete = await find_list(all_lists, list_name, message) 
            if (list_to_complete):
                if (len(list_to_complete) > 0):
                    list_to_complete[0].add_card(name=name_of_card[0])            
    elif len(exploded_msg) == 1:
        await message.channel.send("`/add_card [LIST] [CARD]`")
    elif len(exploded_msg) == 2:
        await message.channel.send("Ayo, you forgot to tell what to add in this list\nIf you forgot how to use, just type `/add_card`")

def check_if_already_exists(board_id, name_of_list):
    all_lists = trello_client.get_board(board_id).all_lists()    
    for liste_to_find in all_lists:
        if liste_to_find.name == name_of_list:
            return 1
    return 0

async def add_list(message):
    exploded_msg = (message.content).split(" ")
    if (len(exploded_msg) == 2):
        name_of_list = exploded_msg[1]
        BOARD_ID = getBoard()
        if check_if_already_exists(BOARD_ID, name_of_list) == 0:
            trello_client.get_board(BOARD_ID).add_list(name_of_list)
            await message.channel.send("The list {} is created !".format(name_of_list))
        else:
            await message.channel.send("The list {} has already been created".format(name_of_list))
    elif (len(exploded_msg) == 1):
        await message.channel.send("`/add_list [LIST]`")
    elif (len(exploded_msg) > 2):
        await message.channel.send("Bro, this command take only one parameter\nIf you forgot how to use it, check `/add_list`")


async def get_list(message):
    msg = ">>> "
    exploded_msg = (message.content).split(" ")
    if (len(exploded_msg) == 1):
        BOARD_ID = getBoard() 
        all_lists = trello_client.get_board(BOARD_ID).all_lists()
        for List in all_lists:
            msg += "{}\n".format(List.name)
        if (len(msg) > 0):
            await message.channel.send(msg)
    else:
        await message.channel.send("Man, this command has no parameter, just run it like that")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/add_card"):
        await add_card(message)
    if message.content.startswith("/add_list"):
        await add_list(message)
    if message.content.startswith("/get_list"):
        await get_list(message)
client.run(config["BOT_TOKEN"])

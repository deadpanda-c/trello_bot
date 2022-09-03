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
            return 1, liste_to_find
    return 0, None

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

async def list_cards(message):
    msg = ">>> "
    exploded_msg = (message.content).split(" ")
    if (len(exploded_msg) == 1):
        await message.channel.send("You forgot a parameter dummies (the list name ;) )")
    elif (len(exploded_msg) == 2):
        # print all the cards from this list
        BOARD_ID = getBoard()
        list_to_print = exploded_msg[1]
        msg = "Here you go with the cards in **{}**\n>>> ".format(list_to_print.replace("\n", ""))
        error_code, list_to_list = check_if_already_exists(BOARD_ID, list_to_print)
        if error_code== 1:
            all_cards_in_this_list = list_to_list.list_cards()
            for card in all_cards_in_this_list:
                card_name = card.name
                card_description = (card.description).replace("\n", "") if len(card.description) > 0 else "No description"
                msg += "{}: *{}* \n".format(card_name, card_description)
            await message.channel.send(msg)
        else:
            await message.channel.send("Man, your list doesn't exist :(")
    else:
        await message.channel.send("There is too much parameter")

async def display_help(message):
    await message.channel.send(">>> Welcome dear user !\nSoooo, here is my man ! Enjoy :) !\n\n`/add_card [LIST] [name of your card]`: allows you to add a card in a existing list in the board\n`/add_list [LIST]`: If a list doesn't exist, you can create it by running this command\n`/get_list`: allows you to get the list of list (i'm too funny dude)\n`/get_cards`: if you don't remember what you put on your trello (shame on you), you can just get it by tapping this command\n`/\\help`: Am I really supposed to describe what it does ??")


@client.event
async def on_ready():
    channel = client.get_channel(int(config["CHANNEL_ID"]))
    if not channel:
        print("No channel found")
    else:
        await channel.send("""
        >>> Hello everyone, I'm up !! :smile:\nI'm here to help y'all for this amazing project (lol) ! If you want to see my incredible power, just type `/\\help` !\nAnd now, Good Luck for this project, and Enjoy ! :)\n
        
        https://giphy.com/gifs/foxhomeent-napoleon-dynamite-20th-century-fox-icUEIrjnUuFCWDxFpU
        """)
        print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("/\\help"):
        await display_help(message)
    if message.content.startswith("/add_card"):
        await add_card(message)
    if message.content.startswith("/add_list"):
        await add_list(message)
    if message.content.startswith("/get_list"):
        await get_list(message)
    if message.content.startswith("/get_cards"):
        await list_cards(message)
    if message.content.startswith("/add_list"):
        # add list (/add_list [nameOfTheFuturList]
        pass
client.run(config["BOT_TOKEN"])

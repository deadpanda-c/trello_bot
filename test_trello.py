from trello import TrelloClient
from dotenv import dotenv_values

config = dotenv_values(".env") # load var in the .env file

client = TrelloClient(
        api_key=config["API_KEY"],
        api_secret=config["API_SECRET"],
        token=config["TOKEN"]
        )

current_boards = None

all_boards = client.list_boards()
for boards in all_boards:
    if boards.name == "Cpp Game":
        current_boards = boards.name
        break

if not current_boards:
    print("No boards found")
else:
    print("Found") 

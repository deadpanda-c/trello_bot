from trello import TrelloClient
from dotenv import dotenv_values

config = dotenv_values(".env") # load var in the .env file


BOARD_ID = None
current_boards = None
is_board_closed = False

LIST = "coucou"

all_boards = client.list_boards()
for boards in all_boards:
    if boards.name == "Cpp Game" and not boards.closed:
        current_boards = boards.name
        BOARD_ID = boards.id 
        all_lists = client.get_board(BOARD_ID).all_lists()
        list_to_complete = [final_list for final_list in all_lists if final_list.name == LIST] 
        card_to_add = list_to_complete[0].add_card(name="ceci est un test", desc="J'AI AJOUTÉ CETTE CARTE EN PYTHON")

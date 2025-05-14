SELECTED_GAME: str = None  

def set_selected_game(game: str) -> None:
    global SELECTED_GAME
    SELECTED_GAME = game

def get_selected_game() -> str:
    global SELECTED_GAME
    return SELECTED_GAME
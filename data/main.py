from . import prepare,tools
from .states import title_screen, gameplay, view_book, create_book


def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "GAMEPLAY": gameplay.Gameplay(),
                   "VIEW_BOOK": view_book.ViewBook(),
                   "CREATE_BOOK": create_book.CreateBook()}
    controller.setup_states(states, "TITLE")
    controller.main()

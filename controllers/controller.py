from controllers.base_mode import IMode
from controllers.text_mode import TextMode
from controllers.command_mode import CommandMode
from controllers.input_mode import InputMode
from controllers.search_mode import SearchMode
from models.search_model import SearchModel
from models.text_model import TextModel
from models.command_model import CommandModel
from views.text_view import TextView
from views.command_view import CommandView
from views.search_view import SearchView
from adapter.interface_tui import ITUI


class Controller:
    def __init__(self, tui: ITUI):
        self.tui = tui
        self.text_model = TextModel()
        self.command_model = CommandModel()
        self.search_model = SearchModel()
        self.text_view = TextView(tui)
        self.command_view = CommandView(tui)
        self.search_view = SearchView(tui)
        self.text_mode = TextMode(self)
        self.command_mode = CommandMode(self)
        self.input_mode = InputMode(self)
        self.search_mode = SearchMode(self)
        self.current_mode = self.text_mode
        self.running = True

    def set_mode(self, mode: IMode):
        self.current_mode.exit()
        self.current_mode = mode
        self.current_mode.enter()

    def exit_program(self):
        self.running = False

    def run(self):
        self.current_mode.enter()
        self.current_mode.update_view()
        while self.running:
            key = self.tui.get_key()
            self.current_mode.handle_input(key)
            self.current_mode.update_view()

from controllers.base_mode import IMode
from controllers.normal_mode import NormalMode
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
from adapter.interface_control import IControl


class Controller:
    def __init__(self, tui: ITUI, control: IControl):
        self.tui = tui
        self.control = control
        self.text_model = TextModel()
        self.command_model = CommandModel()
        self.search_model = SearchModel()
        self.text_view = TextView(tui)
        self.command_view = CommandView(tui)
        self.search_view = SearchView(tui)
        self.text_mode = NormalMode(self)
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

    def update_viewport(self):
        cursor_row, cursor_col = self.text_model.cursor.get_position()
        self.text_view.scroll_to_cursor(cursor_row, cursor_col, self.text_model)

    def run(self):
        self.current_mode.enter()
        self.current_mode.update_view()
        while self.running:
            key = self.control.get_key()
            self.current_mode.handle_input(key)
            self.update_viewport()
            self.current_mode.update_view()

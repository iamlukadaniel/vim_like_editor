from interfaces.modes import IMode
from modes import NormalMode, CommandMode, InputMode, SearchMode, HelpMode
from interfaces.models import ISearchModel, ITextModel, ICommandModel
from models import SearchModel, TextModel, CommandModel
from views import TextView, CommandView, SearchView
from interfaces.adapter import ITUI, IControl


class Controller:
    def __init__(self, tui: ITUI, control: IControl):
        self.tui: ITUI = tui
        self.control: IControl = control

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
        self.help_mode = HelpMode(self)

        self.current_mode = self.text_mode
        self.running = True

    def set_mode(self, mode: IMode) -> None:
        self.current_mode.exit()
        self.current_mode = mode
        self.current_mode.enter()

    def exit_program(self) -> None:
        self.running = False

    def update_viewport(self) -> None:
        cursor_row, cursor_col = self.text_model.get_cursor_position()
        self.text_view.scroll_to_cursor(cursor_row, cursor_col, self.text_model)

    def run(self) -> None:
        self.current_mode.enter()
        self.current_mode.update_view()
        while self.running:
            key = self.control.get_key()
            self.current_mode.handle_input(key)
            self.update_viewport()
            self.current_mode.update_view()

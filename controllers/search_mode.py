from controllers.base_mode import IMode
from utils.keys import Keys


class SearchMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == Keys.ESCAPE:
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.controller.text_model.find_matches(self.controller.search_model.search_text.c_str())
            if self.controller.search_model.is_reversed:
                self.controller.text_model.move_to_previous_match()
            else:
                self.controller.text_model.move_to_next_match()
            self.controller.set_mode(self.controller.text_mode)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.search_model.add_char(char)

    def enter(self):
        self.controller.search_model.clear()
        self.controller.search_view.display(self.controller.search_model)
        self.controller.search_view.update_cursor(0, self.controller.search_model.cursor.col)

    def update_view(self):
        self.controller.search_view.display(self.controller.search_model)
        self.controller.search_view.update_cursor(0, self.controller.search_model.cursor.col)
        pass

    def exit(self):
        self.controller.text_view.display_status("")
        pass

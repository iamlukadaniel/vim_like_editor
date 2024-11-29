from controllers.base_mode import IMode
from utils.keys import Keys


# TODO: придумать обработку команд по типу gg, 10G, yw, diw
class NormalMode(IMode):
    def __init__(self, controller):
        self.controller = controller
        self.is_searching = False

    def handle_input(self, key):
        if key == Keys.DOWN:
            self.controller.text_model.move_cursor(1, 0)
        elif key == Keys.UP:
            self.controller.text_model.move_cursor(-1, 0)
        elif key == Keys.LEFT:
            self.controller.text_model.move_cursor(0, -1)
        elif key == Keys.RIGHT:
            self.controller.text_model.move_cursor(0, 1)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            if key[1] == ':':
                self.controller.set_mode(self.controller.command_mode)
            elif key[1] == 'i':
                self.controller.set_mode(self.controller.input_mode)
            elif key[1] == '/':
                self.controller.search_model.is_reversed = False
                self.controller.set_mode(self.controller.search_mode)
                self.controller.search_model.is_dir_right = True
                self.is_searching = True
            elif key[1] == '?':
                self.controller.search_model.is_reversed = True
                self.controller.set_mode(self.controller.search_mode)
                self.controller.search_model.is_dir_right = False
                self.is_searching = True
            elif key[1] == 'n':
                if self.controller.search_model.is_reversed:
                    self.controller.search_model.is_dir_right = False
                    self.controller.text_model.move_to_previous_match()
                else:
                    self.controller.search_model.is_dir_right = True
                    self.controller.text_model.move_to_next_match()
                self.is_searching = True
            elif key[1] == 'N':
                if self.controller.search_model.is_reversed:
                    self.controller.search_model.is_dir_right = True
                    self.controller.text_model.move_to_next_match()
                else:
                    self.controller.search_model.is_dir_right = False
                    self.controller.text_model.move_to_previous_match()
                self.is_searching = True

    def enter(self):
        self.controller.text_view.display_status("")
        self.controller.text_view.display(self.controller.text_model)
        self.controller.text_view.update_cursor(self.controller.text_model.cursor.row,
                                                self.controller.text_model.cursor.col)

    def update_view(self):
        self.controller.text_view.display(self.controller.text_model)

        if self.is_searching:
            self.is_searching = False
            self.controller.search_view.display(self.controller.search_model)

        self.controller.text_view.update_cursor(
            self.controller.text_model.cursor.row, self.controller.text_model.cursor.col
        )

    def exit(self):
        pass

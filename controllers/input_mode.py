from controllers.base_mode import IMode
from utils.keys import Keys


class InputMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == Keys.ESCAPE:
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.controller.text_model.insert_text('\n')
        elif key == Keys.BACKSPACE:
            self.controller.text_model.delete_char_before_cursor()
        elif key == Keys.DELETE:
            self.controller.text_model.delete_char_after_cursor()
        elif key == Keys.DOWN:
            self.controller.text_model.move_cursor(1, 0)
        elif key == Keys.UP:
            self.controller.text_model.move_cursor(-1, 0)
        elif key == Keys.LEFT:
            self.controller.text_model.move_cursor(0, -1)
        elif key == Keys.RIGHT:
            self.controller.text_model.move_cursor(0, 1)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.text_model.insert_text(char)

    def enter(self):
        self.update_view()

    def update_view(self):
        self.controller.text_view.display(self.controller.text_model)
        self.controller.text_view.display_status("-- INSERT MODE --")
        self.controller.text_view.update_cursor(
            self.controller.text_model.cursor.row, self.controller.text_model.cursor.col
        )

    def exit(self):
        self.controller.text_view.display_status("")

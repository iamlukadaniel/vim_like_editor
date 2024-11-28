from controllers.base_mode import IMode
from utils.keys import Keys


class CommandMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == Keys.ESCAPE:
            self.controller.command_model.clear()
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.controller.command_model.execute_command(self.controller)
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.BACKSPACE:
            command_text = self.controller.command_model.command_text
            if command_text.size() > 0:
                command_text.erase(command_text.size() - 1, 1)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.command_model.add_char(char)

    def enter(self):
        self.controller.command_model.clear()
        self.controller.command_view.display(self.controller.command_model)
        self.controller.command_view.update_cursor(0, self.controller.command_model.cursor.col)

    def update_view(self):
        self.controller.command_view.display(self.controller.command_model)
        self.controller.command_view.update_cursor(0, self.controller.command_model.cursor.col)

    def exit(self):
        self.controller.text_view.display_status("")

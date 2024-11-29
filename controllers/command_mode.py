from controllers.base_mode import IMode
from utils.keys import Keys


class CommandMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key):
        if key == Keys.LEFT:
            self.controller.command_model.move_cursor(-1)
        elif key == Keys.RIGHT:
            self.controller.command_model.move_cursor(1)
        elif key == Keys.ESCAPE:
            self.controller.command_model.clear()
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.execute_command()
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.BACKSPACE:
            self.controller.command_model.delete_char_before_cursor()
        elif key == Keys.DELETE:
            self.controller.command_model.delete_char_after_cursor()
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.command_model.add_char(char)

    def execute_command(self):
        command = self.controller.command_model.command_text.c_str().strip()
        if command == 'q':
            self.controller.exit_program()
        elif command.startswith('w'):
            filename = command[1:].strip() or 'default.txt'
            self.controller.text_model.save_file(filename)
        elif command.startswith('o'):
            filename = command[1:].strip() or 'default.txt'
            self.controller.text_model.load_file(filename)
        # Implement other commands as per requirements
        self.controller.command_model.clear()

    def enter(self):
        self.controller.command_model.clear()
        self.controller.command_view.display(self.controller.command_model)
        self.controller.command_view.update_cursor(0, self.controller.command_model.cursor.col)

    def update_view(self):
        self.controller.command_view.display(self.controller.command_model)
        self.controller.command_view.update_cursor(0, self.controller.command_model.cursor.col)

    def exit(self):
        self.controller.text_view.display_status("")

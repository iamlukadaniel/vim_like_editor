from typing import Tuple

from interfaces.modes.base_mode import IMode
from utils.keys import Keys
from MyString import MyString


class CommandMode(IMode):
    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, key: Keys | Tuple[Keys, str]) -> None:
        if key == Keys.LEFT:
            self.controller.command_model.move_cursor(-1)
        elif key == Keys.RIGHT:
            self.controller.command_model.move_cursor(1)
        elif key == Keys.ESCAPE:
            self.controller.command_model.clear()
            self.controller.set_mode(self.controller.text_mode)
        elif key == Keys.ENTER:
            self.execute_command()
        elif key == Keys.BACKSPACE:
            self.controller.command_model.delete_char_before_cursor()
        elif key == Keys.DELETE:
            self.controller.command_model.delete_char_after_cursor()
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            self.controller.command_model.add_char(char)

    def execute_command(self) -> None:
        command = self.controller.command_model.get_command_text().c_str().strip()
        if command == 'q':
            self.quit_program()
        elif command == 'q!':
            self.force_quit_program()
        elif command == 'x' or command == 'wq!':
            self.save_quit()
        elif command.startswith('w'):
            filename = command[1:].strip() or 'default.txt'
            self.save_to(filename)
        elif command.startswith('o'):
            filename = command[1:].strip()
            self.open_file(filename)
        elif command == 'h':
            self.open_help()
            return
        elif command.is_digit():
            self.go_to_line_n(int(command))
        self.controller.command_model.clear()
        self.controller.set_mode(self.controller.text_mode)

    def open_help(self) -> None:
        self.controller.set_mode(self.controller.help_mode)

    def force_quit_program(self) -> None:
        self.controller.exit_program()

    def save_quit(self) -> None:
        current_file = self.controller.command_model.get_current_file()
        if current_file.empty():
            self.controller.text_model.save_file('default.txt')
        else:
            self.controller.text_model.save_file(current_file.c_str())
        self.controller.exit_program()

    def go_to_line_n(self, n: int) -> None:
        self.controller.text_model.go_to_line_n(n)

    def save_to(self, filename: str) -> None:
        self.controller.text_model.save_file(filename)

    def open_file(self, filename: str) -> None:
        if not filename:
            return
        self.controller.command_model.set_current_file(filename)
        self.controller.text_model.load_file(filename)

    def quit_program(self) -> None:
        if self.controller.text_model.is_modified():
            return
        self.controller.exit_program()

    def enter(self) -> None:
        self.controller.command_model.clear()
        self.controller.command_view.display(self.controller.command_model)
        row, col = self.controller.command_model.get_cursor_position()
        self.controller.command_view.update_cursor(row, col)

    def update_view(self) -> None:
        self.controller.command_view.display(self.controller.command_model)
        row, col = self.controller.command_model.get_cursor_position()
        self.controller.command_view.update_cursor(row, col)

    def exit(self) -> None:
        self.controller.text_view.display_status("")

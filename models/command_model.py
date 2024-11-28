from MyString import MyString
from models.cursor_model import CursorModel


# TODO: 1. Перенести execute_command по соответствующим режимам
#       2. Дополнить нужными методами
class CommandModel:
    def __init__(self):
        self.cursor = CursorModel()
        self.command_text = MyString()

    def add_char(self, char: str):
        self.command_text += char
        self.cursor.col += 1

    def clear(self):
        self.command_text.clear()
        self.cursor.col = 0

    def execute_command(self, controller):
        command = self.command_text.c_str().strip()
        if command == 'q':
            controller.exit_program()
        elif command.startswith('w'):
            filename = command[1:].strip() or 'default.txt'
            controller.text_model.save_file(filename)
        # Implement other commands as per requirements
        self.clear()

from typing import Tuple

from interfaces.modes.base_mode import IMode
from utils.keys import Keys
from trie.command_trie import CommandTrie


class NormalMode(IMode):
    def __init__(self, controller):
        self.controller = controller
        self.is_searching: bool = False
        self.is_line_copied: bool = False
        self.trie: CommandTrie = CommandTrie()
        self.build_trie()

    def build_trie(self) -> None:
        self.trie.insert(':', self.set_command_mode)
        self.trie.insert('i', self.set_input_mode)
        self.trie.insert('I', self.set_input_from_line_start)
        self.trie.insert('A', self.set_input_from_line_end)
        self.trie.insert('S', self.set_input_after_line_erase)
        self.trie.insert('r', self.replace_char_under_cursor)
        self.trie.insert('/', self.set_search_mode)
        self.trie.insert('?', self.set_reversed_search_mode)
        self.trie.insert('^', self.go_to_line_start)
        self.trie.insert('0', self.go_to_line_start)
        self.trie.insert('$', self.go_to_line_end)
        self.trie.insert('x', self.delete_char_after_cursor)
        self.trie.insert('dd', self.cut_current_line)
        self.trie.insert('yy', self.yank_current_line)
        self.trie.insert('yw', self.yank_word)
        self.trie.insert('p', self.paste)
        self.trie.insert('n', self.go_to_next_search_match)
        self.trie.insert('N', self.go_to_prev_search_match)
        self.trie.insert('e', self.go_to_word_end)
        self.trie.insert('b', self.go_to_word_start)
        self.trie.insert('gg', self.go_to_file_start)
        self.trie.insert('G', self.go_to_file_end)
        self.trie.insert('diw', self.delete_inner_word)

    def handle_input(self, key: Keys | Tuple[Keys, str]) -> None:
        if key in [Keys.UP, Keys.DOWN, Keys.RIGHT, Keys.LEFT]:
            self.process_navigation_key(key)
        elif isinstance(key, tuple) and key[0] == Keys.CHAR:
            char = key[1]
            command_model = self.controller.command_model

            if command_model.get_awaiting_argument_for() == 'r':
                self.replace_char_under_cursor(char)
                command_model.set_awaiting_argument_for(None)
                command_model.clear()
                return

            if char in "123456789":
                if command_model.get_command_count() is None:
                    command_model.set_command_count(0)
                command_model.set_command_count(command_model.get_command_count() * 10 + int(char))
                command_model.add_char(char)
                return

            command_model.add_char(char)
            cmd_text = command_model.get_command_text().c_str()
            for i in "123456789":
                cmd_text = cmd_text.replace(i, '')
            command, is_prefix = self.trie.search(cmd_text)

            if command:
                if cmd_text == 'r':
                    command_model.set_awaiting_arg_for('r')
                    return

                if cmd_text == 'G' and command_model.get_command_count():
                    line_number = command_model.get_command_count()
                    command_model.set_command_count(None)
                    command_model.clear()
                    self.go_to_line_n(line_number)
                    return

                command_model.set_command_count(None)
                command_model.clear()
                command()
            elif not is_prefix:
                command_model.set_command_count(None)
                command_model.clear()

    def process_navigation_key(self, key: Keys) -> None:
        if key == Keys.DOWN:
            self.controller.text_model.move_cursor(1, 0)
        elif key == Keys.UP:
            self.controller.text_model.move_cursor(-1, 0)
        elif key == Keys.LEFT:
            self.controller.text_model.move_cursor(0, -1)
        elif key == Keys.RIGHT:
            self.controller.text_model.move_cursor(0, 1)

    def set_command_mode(self) -> None:
        self.controller.set_mode(self.controller.command_mode)

    def set_input_mode(self) -> None:
        self.controller.set_mode(self.controller.input_mode)

    def set_input_from_line_start(self) -> None:
        self.controller.text_model.go_to_line_start()
        self.controller.set_mode(self.controller.input_mode)

    def set_input_from_line_end(self) -> None:
        self.controller.text_model.go_to_line_end()
        self.controller.set_mode(self.controller.input_mode)

    def set_input_after_line_erase(self) -> None:
        self.controller.text_model.erase_line()
        self.controller.text_model.insert_empty_line()
        self.controller.set_mode(self.controller.input_mode)

    def replace_char_under_cursor(self, char) -> None:
        self.controller.text_model.delete_char_after_cursor()
        self.controller.text_model.insert_text(char)
        self.controller.text_model.move_cursor(0, -1)

    def set_search_mode(self) -> None:
        self.controller.search_model.set_reversed(False)
        self.controller.set_mode(self.controller.search_mode)
        self.controller.search_model.set_dir_right(True)
        self.is_searching = True

    def set_reversed_search_mode(self) -> None:
        self.controller.search_model.set_reversed(True)
        self.controller.set_mode(self.controller.search_mode)
        self.controller.search_model.is_dir_right_flag = False
        self.is_searching = True

    def go_to_line_n(self, n) -> None:
        self.controller.text_model.go_to_line_n(n - 1)

    def go_to_line_start(self) -> None:
        self.controller.text_model.go_to_line_start()

    def go_to_line_end(self) -> None:
        self.controller.text_model.go_to_line_end()

    def delete_char_after_cursor(self) -> None:
        self.controller.text_model.delete_char_after_cursor()

    def cut_current_line(self) -> None:
        if self.controller.text_model.copy_line():
            self.is_line_copied = True
        self.controller.text_model.erase_line()

    def yank_current_line(self) -> None:
        if self.controller.text_model.copy_line():
            self.is_line_copied = True

    def yank_word(self) -> None:
        if self.controller.text_model.copy_word():
            self.is_line_copied = False

    def paste(self) -> None:
        if self.is_line_copied:
            self.controller.text_model.paste_line()
        else:
            self.controller.text_model.paste_word()

    def go_to_next_search_match(self) -> None:
        if self.controller.search_model.is_reversed():
            self.controller.search_model.set_dir_right(False)
            self.controller.text_model.move_to_previous_match()
        else:
            self.controller.search_model.set_dir_right(True)
            self.controller.text_model.move_to_next_match()
        self.is_searching = True

    def go_to_prev_search_match(self) -> None:
        if self.controller.search_model.is_reversed():
            self.controller.search_model.set_dir_right(True)
            self.controller.text_model.move_to_next_match()
        else:
            self.controller.search_model.set_dir_right(False)
            self.controller.text_model.move_to_previous_match()
        self.is_searching = True

    def go_to_word_end(self) -> None:
        self.controller.text_model.go_to_next_word_end()

    def go_to_word_start(self) -> None:
        self.controller.text_model.go_to_prev_word_start()

    def go_to_file_start(self) -> None:
        self.controller.text_model.go_to_file_start()

    def go_to_file_end(self) -> None:
        self.controller.text_model.go_to_file_end()

    def delete_inner_word(self) -> None:
        self.controller.text_model.delete_word_under_cursor()

    def enter(self) -> None:
        self.controller.text_model.move_cursor(0, 0)
        self.controller.text_view.display(self.controller.text_model)
        row, col = self.controller.text_model.get_cursor_position()
        self.controller.text_view.update_cursor(row, col)

    def update_view(self) -> None:
        self.controller.text_model.move_cursor(0, 0)
        self.controller.text_view.display(self.controller.text_model)

        if self.is_searching:
            self.is_searching = False
            self.controller.search_view.display(self.controller.search_model)

        row, col = self.controller.text_model.get_cursor_position()
        self.controller.text_view.update_cursor(row, col)

    def exit(self) -> None:
        pass

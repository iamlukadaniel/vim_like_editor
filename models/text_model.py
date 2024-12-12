from MyString import MyString
from models.cursor_model import CursorModel
from interfaces.models import ITextModel
from typing import Tuple


class TextModel(ITextModel):
    def __init__(self):
        self.cursor: CursorModel = CursorModel()
        self.lines: list[MyString] = []
        self.buffer: MyString = MyString()
        self.matches: list[Tuple[int, int]] = []
        self.is_modified_flag: bool = False

    def get_lines(self) -> list:
        return self.lines

    def is_modified(self) -> bool:
        return self.is_modified_flag

    def load_file(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as file:
            self.lines = [MyString(line.rstrip('\n')) for line in file]
        self.cursor.row, self.cursor.col = 0, 0
        self.is_modified_flag = False

    def save_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            for line in self.lines:
                file.write(line.c_str() + '\n')

    def get_line(self, line: int) -> MyString:
        if 0 <= line < len(self.lines):
            return self.lines[line]
        return MyString()

    def copy_line(self) -> bool:
        if not self.lines:
            return False
        self.buffer = MyString(self.lines[self.cursor.row])
        return True

    def copy_word(self) -> bool:
        if not self.lines:
            return False
        current_line = self.lines[self.cursor.row]
        start = self.cursor.col
        end = current_line.find(' ', start)
        if end == MyString.npos:
            end = current_line.size()
        self.buffer = MyString(current_line.substr(start, end - start))
        return True

    def paste_word(self) -> None:
        if self.buffer.empty():
            return
        self.move_cursor_input(0, 1)
        self.insert_text(self.buffer.c_str())

    def paste_line(self) -> None:
        if self.buffer.empty():
            return
        self.lines.insert(self.cursor.row + 1, MyString(self.buffer))
        self.move_cursor(1, 0)

    def insert_text(self, text: str) -> None:
        if not self.lines:
            self.lines.append(MyString())

        for char in text:
            current_line = self.lines[self.cursor.row]
            if char == '\n':
                if self.cursor.col < current_line.size():
                    new_line = MyString(current_line.substr(self.cursor.col))
                    current_line.erase(self.cursor.col, current_line.size() - self.cursor.col)
                else:
                    new_line = MyString()

                self.lines.insert(self.cursor.row + 1, new_line)
                self.cursor.row += 1
                self.cursor.col = 0
            else:
                if self.cursor.col <= current_line.size():
                    current_line.insert(self.cursor.col, char)
                    self.cursor.col += 1
        self.is_modified_flag = True

    def find_matches(self, text: str) -> None:
        results = []
        for row_num, line in enumerate(self.lines):
            col = line.find(text)
            while col != MyString.npos:
                results.append((row_num, col))
                col = line.find(text, col + 1)
        self.matches = results

    def delete_char_after_cursor(self) -> None:
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)
        elif self.cursor.row + 1 < len(self.lines):
            next_line = self.lines.pop(self.cursor.row + 1)
            current_line.append(next_line.c_str())
        self.is_modified_flag = True

    def delete_char_before_cursor(self) -> None:
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        if self.cursor.col > 0:
            self.move_cursor(0, -1)
            current_line.erase(self.cursor.col, 1)
        elif self.cursor.row > 0:
            prev_line = self.lines[self.cursor.row - 1]
            prev_line_len = len(prev_line.c_str())
            prev_line.append(current_line.c_str())
            self.lines.pop(self.cursor.row)
            self.set_cursor_position(self.cursor.row - 1, prev_line_len)
        self.is_modified_flag = True

    def insert_empty_line(self) -> None:
        self.lines.insert(self.cursor.row, MyString())
        self.is_modified_flag = True

    def erase_line(self) -> None:
        if self.lines:
            self.lines.pop(self.cursor.row)
            if self.cursor.row >= len(self.lines):
                self.cursor.row = max(0, len(self.lines) - 1)
            self.cursor.col = 0
            self.is_modified_flag = True

    def move_cursor(self, row_offset: int, col_offset: int) -> None:
        self.cursor.row = max(0, min(len(self.lines) - 1, self.cursor.row + row_offset))
        if self.lines:
            line_length = self.lines[self.cursor.row].size()
            self.cursor.col = max(0, min(line_length - 1, self.cursor.col + col_offset))
        else:
            self.cursor.col = 0

    def move_cursor_input(self, row_offset: int, col_offset: int) -> None:
        self.cursor.row = max(0, min(len(self.lines) - 1, self.cursor.row + row_offset))
        if self.lines:
            line_length = self.lines[self.cursor.row].size()
            self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))
        else:
            self.cursor.col = 0

    def set_cursor_position(self, row: int, col: int) -> None:
        row = max(0, min(len(self.lines) - 1, row))
        col = max(0, min(self.lines[row].size(), col))
        self.cursor.set_position(row, col)

    def get_cursor_position(self) -> Tuple[int, int]:
        return self.cursor.get_position()

    def move_to_next_match(self) -> None:
        if not self.matches:
            return

        current_pos = self.cursor.get_position()
        closest_match = None

        for match in self.matches:
            if match > current_pos:
                closest_match = match
                break

        if closest_match:
            self.cursor.set_position(*closest_match)
        else:
            self.cursor.set_position(*self.matches[0])

    def move_to_previous_match(self) -> None:
        if not self.matches:
            return

        current_pos = self.cursor.get_position()
        closest_match = None

        for match in reversed(self.matches):
            if match < current_pos:
                closest_match = match
                break

        if closest_match:
            self.cursor.set_position(*closest_match)
        else:
            self.cursor.set_position(*self.matches[-1])

    def go_to_line_start(self) -> None:
        if not self.lines:
            return
        self.set_cursor_position(self.cursor.row, 0)

    def go_to_line_end(self) -> None:
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        self.set_cursor_position(self.cursor.row, current_line.size())

    def go_to_file_start(self) -> None:
        if not self.lines:
            return
        self.set_cursor_position(0, 0)

    def go_to_file_end(self) -> None:
        if not self.lines:
            return
        last_line_idx = len(self.lines) - 1
        last_line = self.lines[last_line_idx]
        self.set_cursor_position(last_line_idx, last_line.size() - 1)

    def go_to_line_n(self, line_idx: int) -> None:
        if not self.lines:
            return
        self.set_cursor_position(line_idx, self.cursor.col)

    def go_to_next_word_end(self) -> None:
        if not self.lines:
            return

        current_line = self.lines[self.cursor.row]

        while True:
            if not current_line.empty() and current_line[self.cursor.col].isalnum():
                if self.cursor.col != len(current_line) - 1:
                    self.cursor.col += 1
                elif self.cursor.row < len(self.lines) - 1:
                    self.cursor.row += 1
                    current_line = self.lines[self.cursor.row]
                    self.cursor.col = 0
                else:
                    return

            while not current_line.empty() and not current_line[self.cursor.col].isalnum():
                if self.cursor.col < len(current_line) - 1:
                    self.cursor.col += 1
                elif self.cursor.row < len(self.lines) - 1:
                    self.cursor.row += 1
                    current_line = self.lines[self.cursor.row]
                    self.cursor.col = 0
                else:
                    return

            while current_line.empty():
                if self.cursor.row < len(self.lines) - 1:
                    self.cursor.row += 1
                    current_line = self.lines[self.cursor.row]
                    self.cursor.col = 0
                    if not current_line.empty() and current_line[0].isalnum() and len(current_line) == 1:
                        return
                else:
                    return

            while not current_line[self.cursor.col].isalnum() and self.cursor.col != len(current_line) - 1:
                self.cursor.col += 1

            while current_line[self.cursor.col].isalnum() and self.cursor.col != len(current_line) - 1:
                self.cursor.col += 1

            if not current_line[self.cursor.col].isalnum():
                self.cursor.col -= 1

            if current_line[self.cursor.col].isalnum():
                return

            continue

    def go_to_prev_word_start(self) -> None:
        if not self.lines:
            return

        current_line = self.lines[self.cursor.row]

        if current_line.empty():
            if self.cursor.row > 0:
                self.cursor.row -= 1
                current_line = self.lines[self.cursor.row]
                self.cursor.col = max(0, len(current_line) - 1)
                if not current_line.empty() and self.cursor.col == 0 and current_line[0].isalnum():
                    return
            else:
                return

        if current_line.empty():
            return

        if current_line[self.cursor.col].isalnum():
            if self.cursor.col != 0:
                self.cursor.col -= 1
            elif self.cursor.row > 0:
                self.cursor.row -= 1
                current_line = self.lines[self.cursor.row]
                self.cursor.col = max(0, len(current_line) - 1)
                if current_line.empty():
                    return
            else:
                return

        while not current_line[self.cursor.col].isalnum():
            if self.cursor.col > 0:
                self.cursor.col -= 1
            elif self.cursor.row > 0:
                self.cursor.row -= 1
                current_line = self.lines[self.cursor.row]
                self.cursor.col = max(0, len(current_line) - 1)
                if current_line.empty():
                    return
            else:
                return

        while current_line[self.cursor.col].isalnum() and self.cursor.col != 0:
            self.cursor.col -= 1

        if not current_line[self.cursor.col].isalnum():
            self.cursor.col += 1

    def delete_word_under_cursor(self) -> None:
        current_line = self.lines[self.cursor.row]

        start_col = self.cursor.col
        end_col = self.cursor.col

        if current_line.empty():
            return

        if current_line[self.cursor.col].isalnum():
            while start_col > 0 and current_line[start_col - 1].isalnum():
                start_col -= 1
            while end_col < len(current_line) and current_line[end_col].isalnum():
                end_col += 1
        else:
            while start_col > 0 and not current_line[start_col - 1].isalnum():
                start_col -= 1
            while end_col < len(current_line) and not current_line[end_col].isalnum():
                end_col += 1

        if start_col == end_col:
            current_line.erase(start_col, 1)
        else:
            current_line.erase(start_col, end_col - start_col)

        self.cursor.col = start_col
        self.is_modified_flag = True

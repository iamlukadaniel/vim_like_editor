from MyString import MyString
from models.cursor_model import CursorModel


# TODO: 5. справка по командам
class TextModel:
    def __init__(self):
        self.cursor = CursorModel()
        self.lines = []  # List of MyString instances
        self.buffer = MyString()
        self.matches = []

    def load_file(self, filename: str):
        with open(filename, "r", encoding="latin1") as file:
            self.lines = [MyString(line.rstrip('\n')) for line in file]
        self.cursor.row, self.cursor.col = 0, 0

    def save_file(self, filename: str):
        with open(filename, "w", encoding="latin1") as file:
            for line in self.lines:
                file.write(line.c_str() + '\n')

    def get_line(self, line: int) -> MyString:
        if 0 <= line < len(self.lines):
            return self.lines[line]
        return MyString()

    def copy_line(self):
        if not self.lines:
            return
        self.buffer = MyString(self.lines[self.cursor.row])

    def copy_word(self):
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        start = self.cursor.col
        end = current_line.find(' ', start)
        if end == MyString.npos:
            end = current_line.size()
        self.buffer = MyString(current_line.substr(start, end - start))

    def insert_text(self, text: str):
        if not self.lines:
            self.lines.append(MyString())

        for char in text:
            current_line = self.lines[self.cursor.row]
            if char == '\n':
                # Разделяем строку на две части
                if self.cursor.col < current_line.size():
                    new_line = MyString(current_line.substr(self.cursor.col))
                    current_line.erase(self.cursor.col, current_line.size() - self.cursor.col)
                else:
                    # Если cursor.col вне диапазона, создаем пустую строку
                    new_line = MyString()

                self.lines.insert(self.cursor.row + 1, new_line)
                self.cursor.row += 1
                self.cursor.col = 0
            else:
                if self.cursor.col <= current_line.size():
                    current_line.insert(self.cursor.col, char)
                    self.cursor.col += 1

    def find_matches(self, text: str):
        results = []
        for row_num, line in enumerate(self.lines):
            col = line.find(text)
            while col != MyString.npos:
                results.append((row_num, col))
                col = line.find(text, col + 1)
        self.matches = results

    def delete_char_after_cursor(self):
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        if self.cursor.col < current_line.size():
            current_line.erase(self.cursor.col, 1)
        elif self.cursor.row + 1 < len(self.lines):
            # Merge with next line if at the end
            next_line = self.lines.pop(self.cursor.row + 1)
            current_line.append(next_line.c_str())

    def delete_char_before_cursor(self):
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

    def delete_line(self):
        if self.lines:
            self.lines.pop(self.cursor.row)
            if self.cursor.row >= len(self.lines):
                self.cursor.row = max(0, len(self.lines) - 1)
                self.cursor.col = 0

    def move_cursor(self, row_offset: int, col_offset: int):
        self.cursor.row = max(0, min(len(self.lines) - 1, self.cursor.row + row_offset))
        if self.lines:
            line_length = self.lines[self.cursor.row].size()
            self.cursor.col = max(0, min(line_length, self.cursor.col + col_offset))
        else:
            self.cursor.col = 0

    def set_cursor_position(self, row: int, col: int):
        row = max(0, min(len(self.lines) - 1, row))
        col = max(0, min(self.lines[row].size(), col))
        self.cursor.set_position(row, col)

    def move_to_next_match(self):
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

    def move_to_previous_match(self):
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

    def go_to_line_start(self):
        if not self.lines:
            return
        self.set_cursor_position(self.cursor.row, 0)

    def go_to_line_end(self):
        if not self.lines:
            return
        current_line = self.lines[self.cursor.row]
        self.set_cursor_position(self.cursor.row, current_line.size() - 1)

    def go_to_file_start(self):
        if not self.lines:
            return
        self.set_cursor_position(0, 0)

    def go_to_file_end(self):
        if not self.lines:
            return
        last_line_idx = len(self.lines) - 1
        last_line = self.lines[last_line_idx]
        self.set_cursor_position(last_line_idx, last_line.size() - 1)

    def go_to_line(self, line_idx: int):
        if not self.lines:
            return
        self.set_cursor_position(line_idx, self.cursor.col)

    def get_end_of_word(self) -> (int, int):
        if not self.lines:
            return None, None

        current_line = self.lines[self.cursor.row]
        col = self.cursor.col

        while col < current_line.size() and current_line[col] == ' ':
            col += 1

        start_col = col
        while col < current_line.size() and current_line[col] != ' ':
            col += 1

        if col >= current_line.size():
            if self.cursor.row + 1 < len(self.lines):
                return start_col, 0

        return start_col, col

    def get_start_of_word(self) -> (int, int):
        if not self.lines:
            return None, None

        current_line = self.lines[self.cursor.row]
        col = self.cursor.col

        while col > 0 and current_line[col - 1] == ' ':
            col -= 1

        end_col = col
        while col > 0 and current_line[col - 1] != ' ':
            col -= 1

        if col > 0 and current_line[col - 1] == ' ':
            while col > 0 and current_line[col - 1] == ' ':
                col -= 1
            while col > 0 and current_line[col - 1] != ' ':
                col -= 1

        return col, end_col

    def delete_word_under_cursor(self):
        if not self.lines:
            return

        current_line = self.lines[self.cursor.row]

        start_col, end_col = self.get_start_of_word()
        _, next_word_start = self.get_end_of_word()

        if start_col is None or end_col is None:
            return

        if start_col != end_col and current_line[end_col] == ' ':
            while end_col < len(current_line) and current_line[end_col] == ' ':
                end_col += 1

        current_line.erase(start_col, end_col - start_col)

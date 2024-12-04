# views/text_view.py
from adapter.interface_tui import ITUI
from models.text_model import TextModel


class TextView:
    def __init__(self, tui: ITUI):
        self.tui = tui
        self.top_line = 0  # Верхняя строка окна просмотра
        self.left_col = 0
        self.max_y, self.max_x = self.tui.get_screen_size()
        self.max_y -= 1  # Оставляем строку для статуса

    def update_viewport_size(self):
        self.max_y, self.max_x = self.tui.get_screen_size()
        self.max_y -= 1  # Оставляем строку для статуса

    def display(self, model: TextModel):
        self.tui.clear()
        self.update_viewport_size()

        # Начинаем с текущей верхней строки в окне просмотра
        current_display_line = 0
        line_idx = self.top_line

        while line_idx < len(model.lines) and current_display_line < self.max_y:
            line = model.lines[line_idx].c_str()

            # Если строка слишком длинная, отображаем только видимую часть
            visible_part = line[self.left_col:(self.left_col + self.max_x)]
            self.tui.draw(current_display_line, 0, visible_part)

            # Переходим к следующей строке экрана
            current_display_line += 1
            line_idx += 1

        self.tui.refresh()

    def update_cursor(self, row: int, col: int):
        # Переводим модельные координаты в экранные с учетом viewport
        screen_y = row - self.top_line
        screen_x = col - self.left_col

        # Проверяем, что координаты находятся в пределах экрана
        screen_y = max(0, min(self.max_y - 1, screen_y))
        screen_x = max(0, min(self.max_x - 1, screen_x))

        self.tui.move_cursor(screen_y, screen_x)

    def display_status(self, status: str):
        max_y, max_x = self.tui.get_screen_size()
        self.tui.draw(max_y - 1, 0, status.ljust(max_x))
        self.tui.refresh()

    def scroll_to_cursor(self, cursor_row: int, cursor_col: int, model: TextModel):
        # Обновляем top_line и left_col, чтобы курсор был видимым
        if cursor_row < self.top_line:
            self.top_line = cursor_row
        elif cursor_row >= self.top_line + self.max_y:
            self.top_line = cursor_row - self.max_y + 1

        if cursor_col < self.left_col:
            self.left_col = cursor_col
        elif cursor_col >= self.left_col + self.max_x:
            self.left_col = cursor_col - self.max_x + 1

        self.display(model)
        self.update_cursor(cursor_row, cursor_col)

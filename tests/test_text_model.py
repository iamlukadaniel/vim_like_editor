import unittest
from MyString import MyString
from models.text_model import TextModel


class TestTextModel(unittest.TestCase):

    def test_load_file(self):
        text_model = TextModel()
        text_model.load_file('test_file.txt')

        self.assertEqual(len(text_model.lines), 3)
        self.assertEqual(text_model.lines[0].c_str(), "Line 1")

        self.assertEqual(text_model.cursor.row, 0)
        self.assertEqual(text_model.cursor.col, 0)

    def test_save_file(self):
        text_model = TextModel()
        text_model.lines = [MyString("Line 1"), MyString("Line 2")]

        text_model.save_file('test_output.txt')

        with open('test_output.txt', 'r', encoding='latin1') as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "Line 1")
            self.assertEqual(lines[1].strip(), "Line 2")

    def test_get_line_valid_index(self):
        text_model = TextModel()
        text_model.lines = [MyString("Line 1"), MyString("Line 2")]

        line = text_model.get_line(1)
        self.assertEqual(line.c_str(), "Line 2")

    def test_get_line_invalid_index(self):
        text_model = TextModel()
        text_model.lines = [MyString("Line 1"), MyString("Line 2")]

        line = text_model.get_line(10)
        self.assertEqual(line.c_str(), "")

    def test_copy_line(self):
        text_model = TextModel()
        text_model.lines = [MyString("Line 1"), MyString("Line 2")]
        text_model.cursor.row = 1

        text_model.copy_line()

        self.assertEqual(text_model.buffer.c_str(), "Line 2")

    def test_copy_word(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello world")]
        text_model.cursor.row = 0
        text_model.cursor.col = 0

        text_model.copy_word()

        self.assertEqual(text_model.buffer.c_str(), "Hello")

    def test_insert_text(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello world")]
        text_model.cursor.row = 0
        text_model.cursor.col = 5

        text_model.insert_text(" beautiful")

        self.assertEqual(text_model.lines[0].c_str(), "Hello beautiful world")

    def test_insert_newline(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello world")]
        text_model.cursor.row = 0
        text_model.cursor.col = 5

        text_model.insert_text("\nThis is a new line\n")

        self.assertEqual(text_model.lines[0].c_str(), "Hello")
        self.assertEqual(text_model.lines[1].c_str(), "This is a new line")

    def test_find_matches(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello world"), MyString("world again")]

        text_model.find_matches("world")

        self.assertEqual(len(text_model.matches), 2)
        self.assertEqual(text_model.matches[0], (0, 6))
        self.assertEqual(text_model.matches[1], (1, 0))

    def test_delete_char_after_cursor(self):
        text_model = TextModel()
        text_model.lines.append(MyString("Hello world"))
        text_model.cursor.row = 0
        text_model.cursor.col = 5

        text_model.delete_char_after_cursor()

        self.assertEqual(text_model.lines[0].c_str(), 'Helloworld')

    def test_delete_char_before_cursor(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello world")]
        text_model.cursor.row = 0
        text_model.cursor.col = 5

        text_model.delete_char_before_cursor()

        self.assertEqual(text_model.lines[0].c_str(), "Hell world")

    def test_delete_char_before_cursor_merge_lines(self):
        text_model = TextModel()
        text_model.lines = [MyString("Hello"), MyString("world")]
        text_model.cursor.row = 1
        text_model.cursor.col = 0

        text_model.delete_char_before_cursor()

        self.assertEqual(text_model.lines[0].c_str(), "Helloworld")
        self.assertEqual(len(text_model.lines), 1)

    def test_load_file_invalid(self):
        text_model = TextModel()

        with self.assertRaises(FileNotFoundError):
            text_model.load_file('non_existing_file.txt')



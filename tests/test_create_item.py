import unittest
from server.array_database import create_item
from server.commandline import parse_create_item
from server.todo_dataclasses import CompletionType, ToDoItem

class TestParseCreateItem(unittest.TestCase):
    # Can an item be created?
    def test_create_item(self):
        name = "Name"
        description = "Description"
        item = create_item(name, description, None, None, None, None, 0, CompletionType(0))
        self.assertIs(type(item), ToDoItem, "Doesn't return ToDoItem")
        self.assertEqual(item.name, name)
        self.assertEqual(item.description, description)

    def test_too_few_args(self):
        self.assertRaises(ValueError, parse_create_item, [])
        self.assertRaises(ValueError, parse_create_item, ["name"])

    def test_fails_on_only_whitespace(self):
        self.assertRaises(ValueError, parse_create_item, ["", ""])
        self.assertRaises(ValueError, parse_create_item, ["   ", "    "])

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
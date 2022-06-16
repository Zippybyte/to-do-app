import unittest
from server import parse_create_item, create_item

class TestParseCreateItem(unittest.TestCase):

    def test_too_few_args(self):
        self.assertRaises(ValueError, parse_create_item, [])
        self.assertRaises(ValueError, parse_create_item, ["name"])
                
    def test_fails_on_only_whitespace(self):
        self.assertRaises(ValueError, parse_create_item, ["", ""])
        self.assertRaises(ValueError, parse_create_item, ["   ", "    "])


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
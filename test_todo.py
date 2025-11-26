# test_todo.py
import unittest
from todo_app import TodoList

class TestTodoList(unittest.TestCase):
    """Test suite for the TodoList class."""

    def setUp(self):
        """Set up a fresh TodoList instance before each test."""
        self.todo = TodoList()

    def test_add_item(self):
        """Test if items are correctly added to the list."""
        self.todo.add_item("Write code")
        self.assertIn("Write code", self.todo.get_list())
        self.assertEqual(len(self.todo.get_list()), 1)

    def test_add_empty_item(self):
        """Test adding an empty string item (should be prevented)."""
        result = self.todo.add_item("")
        self.assertNotIn("", self.todo.get_list())
        self.assertEqual(result, "Item name cannot be empty")

    def test_complete_item_success(self):
        """Test successful removal of an item."""
        self.todo.add_item("Clean desk")
        result = self.todo.complete_item("Clean desk")
        self.assertTrue(result)
        self.assertNotIn("Clean desk", self.todo.get_list())

    def test_complete_item_not_found(self):
        """Test removal of a non-existent item."""
        self.todo.add_item("Cook dinner")
        result = self.todo.complete_item("Nonexistent task")
        self.assertFalse(result)
        self.assertIn("Cook dinner", self.todo.get_list()) # Check list is unchanged

if __name__ == '__main__':
    # Run all tests verbosely
    unittest.main()
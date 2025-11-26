# todo_app.py
# Simple module to demonstrate a Python application that can be tested.

class TodoList:
    """A simple class to manage a list of to-do items."""
    def __init__(self):
        self.items = []

    def add_item(self, item_name):
        """Adds a new item to the list."""
        if not item_name:
            return "Item name cannot be empty"
        self.items.append(item_name)
        return f"Added: {item_name}"

    def get_list(self):
        """Returns the current list of items."""
        return self.items

    def complete_item(self, item_name):
        """
        Simulates completing an item by removing it from the list.
        Returns True if item was removed, False otherwise.
        """
        try:
            self.items.remove(item_name)
            return True
        except ValueError:
            return False

# Main execution block to run the app in the Docker container
if __name__ == "__main__":
    app = TodoList()
    app.add_item("Buy groceries")
    app.add_item("Finish Jenkinsfile")
    
    print("--- Welcome to the Containerized Todo App ---")
    print(f"Current List: {app.get_list()}")
    
    app.complete_item("Buy groceries")
    print(f"List after completing one task: {app.get_list()}")
    print("App is running successfully.")
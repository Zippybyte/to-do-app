from abc import ABC, abstractmethod
from datetime import datetime
from . import todo_dataclasses

# Definitions
class DatabaseModel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def delete_item(self, index: int):
        """Deletes an item from database."""
        pass

    @abstractmethod
    def edit_field(self, item: todo_dataclasses.ToDoItem, field: str, new_value):
        """Edits an item from the database."""
        pass

    @abstractmethod
    def change_state(self, index: int, new_state: int):
        """Changes an item's completion state."""
        pass

    @abstractmethod
    def get(self, index: int) -> todo_dataclasses.ToDoItem:
        """Gets an item from the database."""
        pass

    @abstractmethod
    def add(self, item: todo_dataclasses.ToDoItem):
        """Adds an item to the database."""
        pass

    @abstractmethod
    def fetch_all(self) -> list[todo_dataclasses.ToDoItem]:
        """Fetches all items from the database."""
        pass



# Data
database: DatabaseModel = None
"""The database currently used by the program."""

# Functions
def create_item(name: str, description: str, repetition: todo_dataclasses.RepeatDate, categories: list[str], tags: list[str], due_by_date: datetime, completion_state: int, completion_type: todo_dataclasses.CompletionType) -> todo_dataclasses.ToDoItem:
    """Creates an ToDoItem and returns it."""
    print(f"Created item {name}")
    
    assert completion_type != None, "completion_type must not be None"
    return todo_dataclasses.ToDoItem(
        0,
        name,
        description,
        repetition,
        categories,
        tags,
        datetime.now,
        due_by_date,
        None,
        completion_state,
        completion_type
    )

def edit_item(item: todo_dataclasses.ToDoItem, field: str, value: str):
    """Edits an item given a item, field, and value."""

    try: 
        new_value = type(getattr(item, field))(value)
    except ValueError:
        raise ValueError("field and value's type must match match")

    old_value = getattr(item, field)
    setattr(item, field, new_value)
    database.edit_field(item, field, new_value)

    print(f"{item}'s {field} is now {new_value} was {old_value}")

def delete_item(index: int):
    """Deletes an item from database."""
    database.delete_item(index)

def edit_field(item: todo_dataclasses.ToDoItem, field: str, new_value):
    """Edits an item from the database."""
    database.edit_field(item, field, new_value)

def change_state(index: int, new_state: int):
    """Changes an item's completion state."""
    database.change_state(index, new_state)

def get(index: int) -> todo_dataclasses.ToDoItem:
    """Gets an item from the database."""
    return database.get(index)

def add(item: todo_dataclasses.ToDoItem):
    """Adds an item to the database."""
    database.add(item)

def fetch_all() -> list[todo_dataclasses.ToDoItem]:
    """Fetches all items from the database."""
    return database.fetch_all()

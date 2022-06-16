from . import todo_dataclasses
from datetime import datetime
from multiprocessing.sharedctypes import Value

todo_items_index: int = 0
todo_items: dict[int, todo_dataclasses.ToDoItem] = {}

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
    database_edit_field(item, field, new_value)

    print(f"{item}'s {field} is now {new_value} was {old_value}")

# Database

def delete_item(index: int):
    """Deletes an item from database."""

    del todo_items[index]
    print(f"Deleted item at index {index}")

def database_edit_field(item: todo_dataclasses.ToDoItem, field: str, new_value):
    """Edits an item from the database."""
    todo_items[item.id] = item

def change_item_state(index: int, new_state: int):
    """Changes an item's completion state."""
    print(f"{get_item(index).completion_state} is now {new_state}")
    
    get_item(index).completion_state = new_state

def get_item(index: int) -> todo_dataclasses.ToDoItem:
    """Gets an item from the database."""
    return todo_items[index]

def add_to_database(item: todo_dataclasses.ToDoItem):
    """Adds an item to the database."""
    global todo_items_index
    item.id = todo_items_index
    todo_items[todo_items_index] = item
    todo_items_index += 1

def fetch_items() -> list[todo_dataclasses.ToDoItem]:
    """Fetches all items from the database."""
    return todo_items.values()

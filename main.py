import todo_dataclasses
from datetime import datetime
from multiprocessing.sharedctypes import Value

todo_items_index: int = 0
todo_items: dict[int, todo_dataclasses.ToDoItem] = {}

def main():

    while True:
        command = input("input command: ")
        commands = command.split()
        if commands[0] == "c":
            parse_create_item(commands[1:])
        elif commands[0] == "e":
            parse_edit_item(commands[1:])
        elif commands[0] == "x":
            parse_change_item_state(commands[1:])
        elif commands[0] == "d":
            delete_item(commands[1:])
        elif commands[0] == "l":
            parse_list_items()
            

# c create
# e edit
# x change
# d delete
# l list

def parse_create_item(args: list[str]):
    if (len(args) < 2):
        print("Not enough args")
        return

    add_to_database(generate_item(args[0], args[1], None, None, None, None, 0, todo_dataclasses.CompletionType(0)))


def generate_item(name: str, description: str, repetition: todo_dataclasses.RepeatDate, categories: list[str], tags: list[str], due_by_date: datetime, completion_state: int, completion_type: todo_dataclasses.CompletionType) -> todo_dataclasses.ToDoItem:
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

def parse_edit_item(args: list[str]):
    try:
        item = get_item(int(args[0]))
    except ValueError:
        print("args[0] is not an int")
        return

    edit_item(item, args[1], args[2])

def edit_item(item: todo_dataclasses.ToDoItem, field: str, value: str):

    try: 
        new_value = type(getattr(item, field))(value)
    except ValueError:
        print("field and value's type don't match")
        return

    old_value = getattr(item, field)
    setattr(item, field, new_value)
    database_edit_field(item, field, new_value)

    print(f"{item}'s {field} is now {new_value} was {old_value}")

def parse_change_item_state(args: list[str]):
    try:
        index = int(args[0])
        new_state = int(args[1])
    except ValueError: 
        print("index or state have to be ints")
        return

    change_item_state(index, new_state)

def parse_delete_item(args: list[str]):
    """Parses arguments from main and runs delete_item."""
    try:
        index = int(args[0])
    except ValueError: 
        return

    delete_item(index)

def delete_item(index: int):
    """Deletes an item from database."""
    print("Delete item")

    del get_item(index)
    print(f"Deleted item at index {index}")

def parse_list_items():
    for item in fetch_items():
        print(item.id, item.name, item.description, item.completion_state)

# Database

def database_edit_field(item: todo_dataclasses.ToDoItem, field: str, new_value):
    todo_items[item.id] = item

def change_item_state(index: int, new_state: int):
    print(f"{get_item(index).completion_state} is now {new_state}")
    
    get_item(index).completion_state = new_state

def get_item(index: int) -> todo_dataclasses.ToDoItem:
    return todo_items[index]

def add_to_database(item: todo_dataclasses.ToDoItem):
    global todo_items_index
    item.id = todo_items_index
    todo_items[todo_items_index] = item
    todo_items_index += 1

def fetch_items() -> list[todo_dataclasses.ToDoItem]:
    return todo_items.values()

if __name__ == "__main__":
    main()
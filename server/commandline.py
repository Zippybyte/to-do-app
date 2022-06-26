from .database import DatabaseModel, add, create_item, get, edit_item, change_state, delete_item, fetch_all
from . import database
from . import array_database, sqlite_database
from . import todo_dataclasses

def main():
    #database.database = array_database.ArrayDatabase()
    database.database = sqlite_database.SQLiteDatabase("todo_list")
    while True:
        command = input("input command: ")
        commands = command.split()
        # try:
        if commands[0] == "c":
            parse_create_item(commands[1:])
        elif commands[0] == "e":
            parse_edit_item(commands[1:])
        elif commands[0] == "x":
            parse_change_item_state(commands[1:])
        elif commands[0] == "d":
            parse_delete_item(commands[1:])
        elif commands[0] == "l":
            list_items()
        elif commands[0] == "q":
            break
        # except Exception as e:
        #     print(e.with_traceback())

# c create
# e edit
# x change
# d delete
# l list

def parse_create_item(args: list[str]):
    """Parses arguments and creates an item."""
    if (len(args) < 2):
        raise ValueError("Not enough args.")
    elif args[0].strip() == "":
        raise ValueError("Name has to contain non-whitespace.")
    
    add(create_item(args[0], args[1], None, None, None, None, 0, todo_dataclasses.CompletionType(0)))

def parse_edit_item(args: list[str]):
    """Parses arguments and edits the value of an item."""
    try:
        item = int(args[0])
    except ValueError:
        raise ValueError("args[0] must be an int")
    
    edit_item(item, args[1], args[2])

def parse_change_item_state(args: list[str]):
    """Parses arguments and changes item state."""
    try:
        index = int(args[0])
        new_state = int(args[1])
    except ValueError:
        raise ValueError("index and state must be ints")
    
    change_state(index, new_state)

def parse_delete_item(args: list[str]):
    """Parses arguments and deletes a given item."""
    try:
        index = int(args[0])
    except ValueError: 
        raise ValueError("args[0] must be an int")

    delete_item(index)

def list_items():
    """Prints all items from database."""
    items = fetch_all()
    if (len(items) == 0):
        return
    for v in items:
        print(v["name"], v["description"])

if __name__ == "__main__":
    main()

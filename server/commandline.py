from .main import add_to_database, create_item, get_item, edit_item, change_item_state, delete_item, fetch_items
from . import todo_dataclasses

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
            parse_delete_item(commands[1:])
        elif commands[0] == "l":
            parse_list_items()

# c create
# e edit
# x change
# d delete
# l list

def parse_create_item(args: list[str]):
    if (len(args) < 2):
        raise ValueError("Not enough args.")
    elif args[0].strip() == "":
        raise ValueError("Name has to contain non-whitespace.")
    
    add_to_database(create_item(args[0], args[1], None, None, None, None, 0, todo_dataclasses.CompletionType(0)))

def parse_edit_item(args: list[str]):
    try:
        item = get_item(int(args[0]))
    except ValueError:
        print("args[0] is not an int")
        return
    
    edit_item(item, args[1], args[2])

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

def parse_list_items():
    for item in fetch_items():
        print(item.id, item.name, item.description, item.completion_state)

if __name__ == "__main__":
    main()

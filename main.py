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
            create_item(commands[1:])
        elif commands[0] == "e":
            edit_item(commands[1:])
        elif commands[0] == "x":
            change_item_state(commands[1:])
        elif commands[0] == "d":
            delete_item(commands[1:])
        elif commands[0] == "l":
            list_items()
            

# c create
# e edit
# x change
# d delete

def create_item(args: list[str]):
    global todo_items_index, todo_items
    print("Create item")
    print(todo_items_index)
    item: todo_dataclasses.ToDoItem = todo_dataclasses.ToDoItem(
        todo_items_index,
        args[0],
        args[1],
        None,
        None,
        None,
        datetime.now,
        None,
        None,
        0,
        todo_dataclasses.CompletionType(0))
    todo_items[todo_items_index] = item
    todo_items_index += 1

def edit_item(args: list[str]):
    print("Edit item")

def complete_item(args: list[str]):
    change_item_state(args)

def change_item_state(args: list[str]):
    print("Change item state")
    try:
        index = int(args[0])
        new_state = int(args[1])
    except ValueError: 
        return
    todo_items[index].completion_state = new_state

def delete_item(args: list[str]):
    print("Delete item")
    try:
        index = int(args[0])
    except ValueError: 
        return
    del todo_items[index]
    print(f"deleted item at index {index}")

def list_items():
    for (index, item) in todo_items.items():
        print(item.id, item.name, item.description, item.completion_state)

if __name__ == "__main__":
    main()
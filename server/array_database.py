from . import todo_dataclasses, database
#from multiprocessing.sharedctypes import Value

todo_items_index: int = 0
todo_items: dict[int, todo_dataclasses.ToDoItem] = {}

class ArrayDatabase(database.DatabaseModel):
    def __init__(self):
        pass

    def delete_item(self, index: int):
        del todo_items[index]
        print(f"Deleted item at index {index}")

    def edit_field(self, item: todo_dataclasses.ToDoItem, field: str, new_value):
        todo_items[item.id] = item

    def change_state(self, index: int, new_state: int):
        print(f"{self.get(index).completion_state} is now {new_state}")
        
        self.get(index).completion_state = new_state

    def get(self, index: int) -> todo_dataclasses.ToDoItem:
        return todo_items[index]

    def add(self, item: todo_dataclasses.ToDoItem):
        global todo_items_index
        item.id = todo_items_index
        todo_items[todo_items_index] = item
        todo_items_index += 1

    def fetch_all(self) -> list[todo_dataclasses.ToDoItem]:
        return todo_items.values()

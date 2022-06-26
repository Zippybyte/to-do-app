import sqlite3
from venv import create
from . import todo_dataclasses, database


class SQLiteDatabase(database.DatabaseModel):
    name = None
    CATEGORY_TABLE_NAME = "todo_category_mapping"

    def create_connection(self) -> sqlite3.Connection:
        connection: sqlite3.Connection = None
        try:
            connection = sqlite3.connect(f"{name}.db")
        except sqlite3.Error as e:
            print(e)
        connection.row_factory = sqlite3.Row
        return connection

    def __init__(self, new_name: str = "todo_list"):
        global name, CATEGORY_TABLE_NAME
        name = new_name
        connection = self.create_connection()
        with connection:
            self.create_table(connection, """CREATE TABLE IF NOT EXISTS todo_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                repetition INTEGER,
                creation_date INTEGER,
                due_by_date INTEGER,
                last_completed INTEGER,
                completion_state INTEGER,
                completion_type INTEGER)""")

            self.create_table(connection, """CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                UNIQUE(id, name))""")

            self.create_table(connection, """CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                UNIQUE(id, name))""")

            self.create_table(connection, """CREATE TABLE IF NOT EXISTS todo_tag_mapping (
                todo_item_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                FOREIGN KEY (todo_item_id) REFERENCES todo_list (id)
                FOREIGN KEY (tag_id) REFERENCES tags (id))""")

            self.create_table(connection, """CREATE TABLE IF NOT EXISTS todo_category_mapping (
                todo_item_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (todo_item_id) REFERENCES todo_list (id)
                FOREIGN KEY (category_id) REFERENCES categories (id))""")

    def create_table(self, connection, create_table_sql: str):
        try:
            cursor = connection.cursor()
            cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)

    def delete_item(self, index: int):
        global name
        cursor = connection.cursor()
        cursor.execute("DELETE FROM {} WHERE id=(?)".format(name), (index,))
        connection.commit()
        print(f"Deleted item at index {index}")

    def edit_field(self, item: todo_dataclasses.ToDoItem, field: str, new_value):
        global name
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE {} SET (?) = (?) WHERE id=(?)".format(name), (field, new_value, item.id))
        connection.commit()

    def change_state(self, index: int, new_state: int):
        print(f"{self.get(index).completion_state} is now {new_state}")
        ##### TODO #####
        self.get(index).completion_state = new_state

    def get(self, index: int) -> todo_dataclasses.ToDoItem:
        global name
        connection = self.create_connection()
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM todo_list WHERE id=(?)", (index,))
        out = cursor.fetchone()
        print (out.keys())
        for i, v in enumerate(out):
            print (i, v)
        return tuple(out)

    def add(self, item: todo_dataclasses.ToDoItem):
        global name, CATEGORY_TABLE_NAME
        connection = self.create_connection()
        cursor = connection.cursor()
        # cursor.execute("INSERT INTO {}(name, description, repetition, creation_date, due_by_date, last_completed, completion_state, completion_type) VALUES(?,?,NULL,?,?,?,?,?)".format(name), (item.name, item.description, item.creation_date, item.due_by_date, item.last_completed, item.completion_state, item.completion_type))
        print(name, item.name, item.description)
        cursor.execute("INSERT INTO {}(name, description, repetition, creation_date, due_by_date, last_completed, completion_state, completion_type) VALUES(?,?,0,0,0,0,0,0)".format(name), (item.name, item.description))
        item_id = cursor.lastrowid
        if item.categories != None:
            for category_id in item.categories:
                cursor.execute("INSERT INTO todo_category_mapping(todo_item_id, category_id) VALUES (?, ?) ON CONFLICT DO NOTHING", (item_id, category_id))
        if item.tags != None:
            for tag_id in item.tags:
                cursor.execute("INSERT INTO todo_tag_mapping(todo_item_id, tag_id) VALUES (?, ?) ON CONFLICT DO NOTHING", (item_id, tag_id))
        connection.commit()

    def fetch_all(self) -> list[todo_dataclasses.ToDoItem]:
        global name
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(name))
        return cursor.fetchall()

    def add_category(self, category: int):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO categories(name) VALUES (?,) ON CONFLICT DO NOTHING", (category))
        connection.commit()

    def add_tag(self, tag: int):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tags(name) VALUES (?,) ON CONFLICT DO NOTHING", (tag))
        connection.commit()

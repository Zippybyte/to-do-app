from flask import Flask, render_template, request, redirect
from . import database, todo_dataclasses, sqlite_database

app = Flask(__name__)
database.database = sqlite_database.SQLiteDatabase("todo_list")


@app.route("/")
def homepage():
    #print(database.todo_items_index)
    return render_template("homepage.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]

        database.add(database.create_item(name, "", None, None, None, None, 0, todo_dataclasses.CompletionType(0)))

        return redirect("/showitems")
    
    return render_template("create.html") 

@app.route("/showitems")
def showitems():
    return render_template("showitems.html", items=database.fetch_all())


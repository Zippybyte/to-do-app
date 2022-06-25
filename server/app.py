from flask import Flask, render_template, request, redirect
from . import main, todo_dataclasses

app = Flask(__name__)

@app.route("/")
def homepage():
    print(main.todo_items_index)
    return render_template("homepage.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]

        main.add_to_database(main.create_item(name, "", None, None, None, None, 0, todo_dataclasses.CompletionType(0)))

        return redirect("/showitems")
    
    return render_template("create.html") 

@app.route("/showitems")
def showitems():
    return render_template("showitems.html", items=main.get_all_items())


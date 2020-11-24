from flask import render_template
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-book")
def add_book():
    return render_template("add_book.html")

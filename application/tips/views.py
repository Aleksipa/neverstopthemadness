from flask import render_template

from application import app, db
from application.tips.models import Tip, Book


@app.route("/tips/edit/tip/<book_id>", methods=["GET"])
def edit_book(book_id):
    book = Book.query.get(book_id)
    return render_template(
        "edit_book.html",
        book=book
    )

@app.route("/tips")
def get_tips():
    return render_template(
        "tips.html",
        tips=db.session().query(Book).all(),
    )

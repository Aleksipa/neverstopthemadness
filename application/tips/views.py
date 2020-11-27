from flask import render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from application import app, db
from application.tips.models import Tip, Book
from application.tips.forms import AddBookForm


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


@app.route("/tips/add-book", methods=["GET", "POST"])
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        db.session().add(Book(
            comment=form.comment.data,
            related_courses=form.related_courses.data,
            tags=form.tags.data,
            title=form.title.data,
            author=form.author.data,
            publication_year=form.publication_year.data,
            isbn=form.isbn.data,
            pages=form.pages.data,
        ))
        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("add_book.html", form=form)

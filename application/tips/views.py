from flask import render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from application import app, db
from application.tips.models import Tip, Book, Video
from application.tips.forms import AddBookForm, AddVideoForm


@app.route("/tips/edit/tip/<tip_id>", methods=["GET"])
def edit_tip(tip_id):
    return render_template(
        "edit_tip.html",
        tip=Tip.query.get(tip_id)
    )



@app.route("/tips")
def get_tips():
    return render_template(
        "tips.html",
        tips=db.session().query(Tip).all(),
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

@app.route("/tips/add-video", methods=["GET", "POST"])
def add_video():
    form = AddVideoForm()

    if form.validate_on_submit():
        db.session().add(Video(
            comment=form.comment.data,
            related_courses=form.related_courses.data,
            tags=form.tags.data,
            title=form.title.data,
            source=form.source.data,
            upload_date=form.upload_date.data
        ))
        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("add_video.html", form=form)

@app.route("/tips/add-audiobook", methods=["GET", "POST"])
def add_audiobook():
    form = AddAudiobookForm()

    if form.validate_on_submit():
        db.session().add(Audiobook(
            comment=form.comment.data,
            related_courses=form.related_courses.data,
            tags=form.tags.data,
            title=form.title.data,
            author=form.author.data,
            narrator=form.narrator.data,
            publication_year=form.publication_year.data,
            isbn=form.isbn.data,
            lengthInSeconds=form.length.data
        ))
        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("add_audiobook.html", form=form)

@app.route("/tips/add", methods=["GET"])
def add():

    return render_template("add_tip.html")

@app.route("/tips_remove/<tip_id>/", methods=["DELETE", "GET"])
def tips_remove(tip_id):

    tip_to_delete = Tip.query.get_or_404(tip_id)

    db.session().delete(tip_to_delete)
    db.session().commit()

    return redirect(url_for("get_tips"))
from flask import render_template, request, abort
from flask.helpers import url_for
from werkzeug.utils import redirect

from application import app, db

from application.tips.models import SearchQuery, Tip, Book, Video, Audiobook, searchable_fields
from application.tips.forms import AddBookForm, AddVideoForm, AddAudiobookForm, validate_search_form




def compute_search_criteria_fields():
    choices = []
    for key, desc in searchable_fields.items():
        choices.append({
            "name": desc.display_name,
            "value": key,
        })
    choices.sort(key=lambda x: x["name"])
    return choices


search_criteria_fields = compute_search_criteria_fields()


@app.route("/")
def get_tips():
    validation_errors = validate_search_form(request.args)
    tips = []
    status = 200
    if validation_errors:
        status = 403
    else:
        if len(request.args) > 0:
            try:
                tips = SearchQuery(request.args).execute()
            except Exception:
                abort(404)
        else:
            tips = Tip.query.all()
    return render_template(
        "tips.html",
        tips=tips,
        filters=list(request.args.items(True)),
        search_fields=search_criteria_fields,
        validation_errors=validation_errors,
    ), status


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
            lengthInSeconds=form.lengthInSeconds.data
        ))
        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("add_audiobook.html", form=form)

@app.route("/tips/add-movie", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()

    if form.validate_on_submit():
        db.session().add(Movie(
            comment=form.comment.data,
            related_courses=form.related_courses.data,
            tags=form.tags.data,
            title=form.title.data,
            director=form.director.data,
            lengthInSeconds=form.lengthInSeconds.data,
            publication_year=form.publication_year.data,

        ))
        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("add_movie.html", form=form)

@app.route("/tips/add", methods=["GET"])
def add():

    return render_template("add_tip.html")


@app.route("/tips_remove/<tip_id>", methods=["DELETE", "GET"])
def tips_remove(tip_id):

    tip_to_delete = Tip.query.get_or_404(tip_id)

    db.session().delete(tip_to_delete)
    db.session().commit()

    return redirect(url_for("get_tips"))


@app.route("/tips/change_read/<tip_id>", methods=["POST"])
def tips_change_read(tip_id):

    tip = Tip.query.get_or_404(tip_id)

    tip.read = not tip.read
    db.session().commit()
    return redirect(url_for("get_tips"))


@app.route("/tips/edit/<tip_id>/", methods=["GET"])
def tips_editform(tip_id):

    tip_to_edit = Tip.query.get_or_404(tip_id)

    if tip_to_edit.type == "Book":
        form = AddBookForm(formdata=request.form, obj=tip_to_edit)
        return render_template("edit_book.html", form=form, tip_id=tip_id)
    else:
        form = AddVideoForm(formdata=request.form, obj=tip_to_edit)
        return render_template("edit_video.html", form=form, tip_id=tip_id)


@app.route("/tips/edit/<tip_id>/", methods=["POST"])
def edit_book_tip(tip_id):

    tip_to_edit = Tip.query.get_or_404(tip_id)

    form = AddBookForm(formdata=request.form, obj=tip_to_edit)

    if form.validate_on_submit():
        tip_to_edit.comment = form.comment.data
        tip_to_edit.related_courses = form.related_courses.data
        tip_to_edit.tags = form.tags.data
        tip_to_edit.title = form.title.data
        tip_to_edit.author = form.author.data
        tip_to_edit.publication_year = form.publication_year.data
        tip_to_edit.isbn = form.isbn.data
        tip_to_edit.pages = form.pages.data

        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("edit_book.html", form=form)


@app.route("/tips/edit/video/<tip_id>/", methods=["POST"])
def edit_video_tip(tip_id):

    tip_to_edit = Tip.query.get_or_404(tip_id)

    form = AddVideoForm(formdata=request.form, obj=tip_to_edit)

    if form.validate_on_submit():
        tip_to_edit.comment = form.comment.data
        tip_to_edit.related_courses = form.related_courses.data
        tip_to_edit.tags = form.tags.data
        tip_to_edit.title = form.title.data
        source = form.source.data
        tip_to_edit.upload_date = form.upload_date.data

        db.session().commit()
        return redirect(url_for("get_tips"))
    return render_template("edit_video.html", form=form)


@app.route("/tips/edit/movie/<tip_id>/", methods=["POST"])
def edit_movie_tip(tip_id):

    tip_to_edit = Tip.query.get_or_404(tip_id)

    form = AddMovieForm(formdata=request.form, obj=tip_to_edit)

    if form.validate_on_submit():
        tip_to_edit.comment = form.comment.data
        tip_to_edit.related_courses = form.related_courses.data
        tip_to_edit.tags = form.tags.data
        tip_to_edit.title = form.title.data
        tip_to_edit.publication_year = form.publication_year.data
        tip_to_edit.director = form.director.data
        tip_to_edit.lengthInSeconds = form.lengthInSeconds.data

        db.session().commit()
        return redirect(url_for("get_tips"))


    return render_template("edit_movie.html", form=form)

@app.route("/tips/edit/audiobook/<tip_id>/", methods=["POST"])
def edit_audiobook_tip(tip_id):

    tip_to_edit = Tip.query.get_or_404(tip_id)

    form = AddAudiobookForm(formdata=request.form, obj=tip_to_edit)

    if form.validate_on_submit():
        tip_to_edit.comment = form.comment.data
        tip_to_edit.related_courses = form.related_courses.data
        tip_to_edit.tags = form.tags.data
        tip_to_edit.title = form.title.data
        tip_to_edit.publication_year = form.publication_year.data
        tip_to_edit.author = form.author.data
        tip_to_edit.narrator = form.narrator.data
        tip_to_edit.isbn = form.isbn.data
        tip_to_edit.lengthInSeconds = form.lengthInSeconds.data

        db.session().commit()
        return redirect(url_for("get_tips"))

    return render_template("edit_audiobook.html", form=form)


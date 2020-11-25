from flask import render_template

from application import app, db
from application.tips.models import Tip, Book


@app.route("/tips")
def get_tips():
    return render_template(
        "tips.html",
        tips=db.session().query(Book).all(),
    )

from ast import Num
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, Optional


class AddTipForm(FlaskForm):
    comment = TextAreaField("Oma kommentti", [Optional()])
    related_courses = StringField("Liittyvät kurssit", [Optional()])
    tags = StringField("Tunnisteet", [Optional()])

    class Meta:
        csrf = False


class AddBookForm(AddTipForm):
    title = StringField("Otsikko", [InputRequired()])
    author = StringField("Kirjailija", [InputRequired()])
    publication_year = IntegerField("Julkaisuvuosi", [Optional()])
    isbn = StringField("ISBN", [Optional()])
    pages = IntegerField("Sivuja", [Optional(), NumberRange(0)])

    class Meta:
        csrf = False

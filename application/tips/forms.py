from ast import Num

from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, TextAreaField
from wtforms.fields.html5 import DateField, URLField

from wtforms.validators import InputRequired, NumberRange, Optional


class AddTipForm(FlaskForm):
    comment = TextAreaField("Oma kommentti", [Optional()])
    related_courses = StringField("Liittyvät kurssit", [Optional()])
    tags = StringField("Tunnisteet", [Optional()])


class AddBookForm(AddTipForm):
    title = StringField("Otsikko", [InputRequired()])
    author = StringField("Kirjailija", [InputRequired()])
    publication_year = IntegerField("Julkaisuvuosi", [Optional()])
    isbn = StringField("ISBN", [Optional()])
    pages = IntegerField("Sivuja", [Optional(), NumberRange(0)])

class AddVideoForm(AddTipForm):
    title = StringField("Otsikko", [InputRequired()])
    source = StringField("URL", [InputRequired()])
    upload_date = DateField("Ladattu", [Optional()])

class AddAudiobookForm(AddTipForm):
    title = StringField("Otsikko", [InputRequired()])
    author = StringField("Kirjailija", [InputRequired()])
    narrator = StringField("Lukija", [Optional()])
    publication_year = IntegerField("Julkaisuvuosi", [Optional()])
    isbn = StringField("ISBN", [Optional()])
    lengthInSeconds = IntegerField("Pituus", [Optional(), NumberRange(0)])

class AddMovieForm(AddTipForm):
    title = StringField("Otsikko", [InputRequired()])
    director = StringField("Ohjaaja", [InputRequired()])
    publication_year = IntegerField("Julkaisuvuosi", [Optional()])
    lengthInSeconds = IntegerField("Pituus", [Optional(), NumberRange(0)])
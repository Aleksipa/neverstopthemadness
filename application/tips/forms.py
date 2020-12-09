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


def validate_search_form(args):
    encountered = set()
    for item in args.items(True):
        if item[0] in encountered:
            return ["Samaa kenttää ei voi hakea useaan kertaan"]
        encountered.add(item[0])
    return []

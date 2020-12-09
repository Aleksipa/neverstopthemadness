from sqlalchemy import func
from sqlalchemy.sql.expression import true

from application import db


class Tip(db.Model):
    __tablename__ = "Tip"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    related_courses = db.Column(db.Text)
    tags = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
    visible = db.Column(db.Boolean, default=True)
    type = db.Column(db.Text)

    __mapper_args__ = {
        "polymorphic_identity": "Tip",
        "polymorphic_on": type,
    }

    display_types = {
        "Tip": "vinkki",
        "Book": "kirja",
        "Video": "video",
        "Audiobook": "äänikirja",
        "Movie": "elokuva"
    }

    # Maps column names to names displayed to the user. If you add new columns
    # to existing models or new models with new column names, remember to add
    # the corresponding display name here.
    column_display_names = {
        "author": "Kirjoittaja",
        "comment": "Kommentti",
        "isbn": "ISBN",
        "lengthInSeconds": "Kesto",
        "narrator": "Lukija",
        "publication_year": "Julkaisuvuosi",
        "pages": "Sivuja",
        "related_courses": "Liittyvät kurssit",
        "source": "Url",
        "tags": "Tunnisteet",
        "title": "Otsikko",
        "upload_date": "Latauspäivämäärä",
        "director": "ohjaaja",
    }

    @staticmethod
    def insert_initial_values():
        if db.session().query(Tip).count() > 0:
            return
        db.session().add(Book(
            title="Clean Code: A Handbook of Agile Software Craftsmanship",
            author="Robert Martin",
            isbn="978-0132350884",
            tags="Ohjelmointi, design patterns",
            related_courses="TKT20006 Ohjelmistotuotanto",
        ))
        db.session().add(Video(
            title="Merge sort algorithm",
            source="https://www.youtube.com/watch?v=TzeBrDU-JaY",
            related_courses="TKT20006 Ohjelmistotuotanto",
            tags="Ohjelmointi, algoritmit"

        ))
        db.session().add(Audiobook(
            title="Python Programming: The Ultimate Beginner's Guide to Master Python Programming Step by Step with Practical Exercices",
            author="Charles Walker",
            narrator="Russell Newton",
            isbn="978-7834915091",
            publication_year=2020,
            tags="Ohjelmointi, python",
            lengthInSeconds=12180
        ))
        db.session().add(Movie(
            title="Monthy Python and the Holy Grail",
            director="Terry Gilliam, Terry Jones",
            publication_year=1975,
            tags="python",
            lengthInSeconds=5520
        ))
        db.session().commit()

    def display_type(self):
        return Tip.display_types[self.type]

    def display_read(self):
        if self.read:
            return "Kyllä"
        return "Ei"


class Book(Tip):
    __tablename__ = "Book"
    __mapper_args__ = {
        "polymorphic_identity": "Book",
    }

    id = db.Column(db.Integer, db.ForeignKey("Tip.id"), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.Text)
    pages = db.Column(db.Integer)


class Video(Tip):
    __tablename__ = "Video"
    __mapper_args__ = {
        "polymorphic_identity": "Video",
    }

    id = db.Column(db.Integer, db.ForeignKey("Tip.id"), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)
    upload_date = db.Column(db.Date)


class Audiobook(Tip):
    __tablename__ = "Audiobook"
    __mapper_args__ = {
        "polymorphic_identity": "Audiobook",
    }

    id = db.Column(db.Integer, db.ForeignKey("Tip.id"), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text, nullable=False)
    narrator = db.Column(db.Text)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.Text)
    lengthInSeconds = db.Column(db.Integer)

class Movie(Tip):
    __tablename__ = "Movie"
    __mapper_args__ = {
        "polymorphic_identity": "Movie",
    }

    id = db.Column(db.Integer, db.ForeignKey("Tip.id"), primary_key=True)
    title = db.Column(db.Text, nullable=False)
    director = db.Column(db.Text, nullable=False)
    publication_year = db.Column(db.Integer)
    lengthInSeconds = db.Column(db.Integer)

class ColumnDescriptor:
    """Contains information about a database table column."""

    def __init__(self, display_name):
        self.display_name = display_name
        self.models = set()

    @staticmethod
    def compute(*columns):
        """Constructs a dict of `ColumnDescriptor`s from a list of column
        objects.
        """
        descriptors = {}
        for column in columns:
            name = column.property.columns[0].name
            model = column.class_
            display_name = Tip.column_display_names[name]

            desc = descriptors.setdefault(name, ColumnDescriptor(display_name))
            desc.models.add(model)
        return descriptors


# This is a list of all fields the user can search. When you add new fields to
# existing models or completely new models, add all user-searchable fields to
# this list.
searchable_fields = ColumnDescriptor.compute(
    Audiobook.author,
    Audiobook.isbn,
    Audiobook.lengthInSeconds,
    Audiobook.narrator,
    Audiobook.publication_year,
    Audiobook.title,

    Book.author,
    Book.isbn,
    Book.pages,
    Book.publication_year,
    Book.title,

    Tip.comment,
    Tip.related_courses,
    Tip.tags,

    Video.source,
    Video.title,
    Video.upload_date,

    Movie.director,
    Movie.lengthInSeconds,
    Movie.publication_year,
    Movie.title,

)


class SearchQuery:
    """Queries the database for tips with filters passed in the constructor.
    Possible fields are listed in `searchable_fields`.
    """

    def __init__(self, fields):
        """`fields` must be a dict-like object of string keys mapped to string
        values."""
        # The resulting filters keyed by table object.
        self.filters = {}
        self.process_fields(fields)

    def process_model(self, model, field, value):
        """Determines the filter to apply for `field` in `model`. `value` is the
        value of the search input for this field."""
        column = getattr(model, field)
        column_type = str(column.property.columns[0].type)
        if column_type == "TEXT":
            return func.lower(column).contains(func.lower(value))
        else:
            return column == value

    def process_fields(self, fields):
        """Processes all fields in `fields`."""
        for field, value in fields.items():
            desc = searchable_fields[field]
            for model in desc.models:
                current_filter = self.filters.setdefault(model, true())
                new_filter = self.process_model(model, field, value)
                self.filters[model] = current_filter & new_filter

    def execute(self):
        """Executes the query. Returns a list of database model instances
        inheriting from `Tip`."""
        results = set()
        for model, filter in self.filters.items():
            results.update(model.query.filter(filter).all())
        return sorted(results, key=lambda x: x.id)

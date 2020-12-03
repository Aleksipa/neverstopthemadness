from os import stat
from application import db


class Tip(db.Model):
    __tablename__ = "Tip"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    related_courses = db.Column(db.Text)
    tags = db.Column(db.Text)
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
        "Audiobook": "äänikirja"
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
            publication_year=2020,
            tags="Ohjelmointi, python",
            lengthInSeconds=12180
        ))
        db.session().commit()

    def display_type(self):
        return Tip.display_types[self.type]


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
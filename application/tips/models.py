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
        db.session().add(Book(
            title="Kirja2",
            author="Robert Martin",
            isbn="123456",
            tags="Ohjelmointi",
            related_courses="TKT20006 Ohjelmistotuotanto",
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

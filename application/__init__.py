from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get("TESTING"):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///local.db",
    )
if not os.environ.get("HEROKU"):
    # This makes the app print all SQL-queries when ran locally
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

from application import views
from application.tips import models, views

db.create_all()

models.Tip.insert_initial_values()

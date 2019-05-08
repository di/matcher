import datetime
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Donation(db.Model):
    id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.Integer)
    currency = db.Column(db.String)
    date = db.Column(db.DateTime)
    status = db.Column(db.String)

    # Additional fields
    name = db.Column(db.String)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable=False)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    donations = db.relationship("Donation", backref="match", lazy=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/_health/")
def health():
    return "So healthy"

import datetime
import os
import datetime

import requests
from flask import Flask, render_template, request, url_for, abort, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from matcher.forms import NewDonationForm, NewMatchForm

DEBUG = os.environ["DEVEL"] == "yes"
THANKS_URL = os.environ["THANKS_URL"]

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
app.debug = DEBUG

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Donation(db.Model):
    id = db.Column(db.String, primary_key=True)
    amount = db.Column(db.String)
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
    goal_dollars = db.Column(db.Integer)
    total_dollars = db.Column(db.Integer, default=0)
    total_cents = db.Column(db.Integer, default=0)


@app.route("/")
def index():
    matches = Match.query.all()
    return render_template("index.html", matches=matches)


@app.route("/new/", methods=["GET", "POST"])
def new_match():
    form = NewMatchForm(request.form)
    if request.method == "POST" and form.validate():
        match = Match(title=form.title.data, goal_dollars=int(form.goal.data))
        db.session.add(match)
        db.session.commit()
        return redirect(url_for("match", match_id=match.id))
    else:
        return render_template("new_match.html", form=form)


@app.route("/match/<match_id>/", methods=["GET", "POST"])
def match(match_id):
    match = db.session.query(Match).get(match_id)
    if not match:
        abort(404)
    form = NewDonationForm(request.form)
    if request.method == "POST" and form.validate():
        transaction_id = form.transaction_id.data
        resp = requests.get(THANKS_URL.format(transaction_id))
        donation = Donation(
            id=transaction_id, name=form.name.data, match_id=match.id, **resp.json()
        )
        db.session.add(donation)
        donation_dollars, donation_cents = [int(x) for x in donation.amount.split('.')]
        total_cents = match.total_cents + donation_cents
        match.total_dollars += donation_dollars + total_cents // 100
        match.total_cents += total_cents % 100

        db.session.commit()
        return redirect(url_for("match", match_id=match.id))
    else:
        return render_template("match.html", match=match, form=form)


@app.route("/_health/")
def health():
    return "So healthy"

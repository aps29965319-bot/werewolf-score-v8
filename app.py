
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","sqlite:///werewolf.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    score = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

    @property
    def win_rate(self):
        total = self.wins + self.losses
        return round((self.wins/total)*100,1) if total else 0

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    players = Player.query.order_by(Player.score.desc()).all()
    return render_template("index.html", players=players)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    if not Player.query.filter_by(name=name).first():
        db.session.add(Player(name=name))
        db.session.commit()
    return redirect("/")

@app.route("/win/<int:id>")
def win(id):
    p = Player.query.get_or_404(id)
    p.score += 3
    p.wins += 1
    db.session.commit()
    return redirect("/")

@app.route("/lose/<int:id>")
def lose(id):
    p = Player.query.get_or_404(id)
    p.losses += 1
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    p = Player.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect("/")

@app.route("/reset")
def reset():
    for p in Player.query.all():
        p.score = p.wins = p.losses = 0
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run()

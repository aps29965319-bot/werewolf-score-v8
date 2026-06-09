
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost/dreamwolf"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    games = db.Column(db.Integer, default=0)
    mvp = db.Column(db.Integer, default=0)
    seer_wins = db.Column(db.Integer, default=0)
    witch_wins = db.Column(db.Integer, default=0)
    guard_wins = db.Column(db.Integer, default=0)
    hunter_wins = db.Column(db.Integer, default=0)
    wolf_wins = db.Column(db.Integer, default=0)
    villager_wins = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    players = Player.query.order_by(Player.score.desc(), Player.wins.desc()).all()
    return render_template('index.html', players=players)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    if name:
        db.session.add(Player(name=name))
        db.session.commit()
    return redirect('/')

def add_stat(pid, col):
    p = Player.query.get_or_404(pid)
    setattr(p, col, getattr(p, col) + 1)
    db.session.commit()

@app.route('/win/<int:pid>')
def win(pid):
    p = Player.query.get_or_404(pid)
    p.score += 3
    p.wins += 1
    p.games += 1
    db.session.commit()
    return redirect('/')

@app.route('/lose/<int:pid>')
def lose(pid):
    p = Player.query.get_or_404(pid)
    p.games += 1
    db.session.commit()
    return redirect('/')

@app.route('/mvp/<int:pid>')
def mvp(pid): add_stat(pid,'mvp'); return redirect('/')
@app.route('/seer/<int:pid>')
def seer(pid): add_stat(pid,'seer_wins'); return redirect('/')
@app.route('/witch/<int:pid>')
def witch(pid): add_stat(pid,'witch_wins'); return redirect('/')
@app.route('/guard/<int:pid>')
def guard(pid): add_stat(pid,'guard_wins'); return redirect('/')
@app.route('/hunter/<int:pid>')
def hunter(pid): add_stat(pid,'hunter_wins'); return redirect('/')
@app.route('/wolf/<int:pid>')
def wolf(pid): add_stat(pid,'wolf_wins'); return redirect('/')
@app.route('/villager/<int:pid>')
def villager(pid): add_stat(pid,'villager_wins'); return redirect('/')

@app.route('/reset/<int:pid>')
def reset(pid):
    p = Player.query.get_or_404(pid)
    p.score=p.wins=p.games=p.mvp=0
    p.seer_wins=p.witch_wins=p.guard_wins=p.hunter_wins=p.wolf_wins=p.villager_wins=0
    db.session.commit()
    return redirect('/')

@app.route('/reset_all')
def reset_all():
    for p in Player.query.all():
        p.score=p.wins=p.games=p.mvp=0
        p.seer_wins=p.witch_wins=p.guard_wins=p.hunter_wins=p.wolf_wins=p.villager_wins=0
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run()

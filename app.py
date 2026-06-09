
from flask import Flask, render_template, request, redirect
import os, sqlite3

app = Flask(__name__)

DB=os.getenv("DB_FILE","dreamwolf.db")

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db=get_db()
    db.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        score INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        games INTEGER DEFAULT 0,
        mvp INTEGER DEFAULT 0,
        seer_wins INTEGER DEFAULT 0,
        witch_wins INTEGER DEFAULT 0,
        guard_wins INTEGER DEFAULT 0,
        hunter_wins INTEGER DEFAULT 0,
        wolf_wins INTEGER DEFAULT 0,
        villager_wins INTEGER DEFAULT 0,
        werewolf_games INTEGER DEFAULT 0
    )
    """)
    db.commit()
    db.close()

init_db()
# 其餘路由沿用原版，可加入狼人場次統計

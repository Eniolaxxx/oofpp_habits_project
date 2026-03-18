# database.py
# handles saving and loading habits from a sqlite database

import sqlite3
from habit import Habit

# database file name
DB = "habits.db"

def connect(db=DB):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    return con

def setup(db=DB):
    # create tables if they dont exist yet
    con = connect(db)
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_at TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)
    
    con.commit()
    con.close()

def add_habit(habit, db=DB):
    # save a new habit to the database
    con = connect(db)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO habits (name, description, periodicity, created_at) VALUES (?, ?, ?, ?)",
        (habit.name, habit.description, habit.periodicity, habit.created_at)
    )
    new_id = cur.lastrowid
    con.commit()
    con.close()
    return new_id

def remove_habit(habit_id, db=DB):
    con = connect(db)
    cur = con.cursor()
    # delete completions first then the habit
    cur.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    cur.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    con.commit()
    con.close()

def add_completion(habit_id, timestamp, db=DB):
    con = connect(db)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
        (habit_id, timestamp)
    )
    con.commit()
    con.close()

def get_all_habits(db=DB):
    # load all habits and their completions from the database
    con = connect(db)
    cur = con.cursor()
    cur.execute("SELECT * FROM habits ORDER BY id")
    rows = cur.fetchall()
    
    habits = []
    for row in rows:
        h = Habit(
            name=row["name"],
            description=row["description"],
            periodicity=row["periodicity"],
            created_at=row["created_at"],
            habit_id=row["id"]
        )
        cur.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (row["id"],))
        h.completions = [c["completed_at"] for c in cur.fetchall()]
        habits.append(h)
    
    con.close()
    return habits

def name_exists(name, db=DB):
    con = connect(db)
    cur = con.cursor()
    cur.execute("SELECT id FROM habits WHERE name = ?", (name,))
    result = cur.fetchone()
    con.close()
    return result is not None

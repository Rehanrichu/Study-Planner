from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create table if not exists
def init_db():
    conn = sqlite3.connect("planner.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    hours INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_subject():
    name = request.form.get("subject")
    hours = int(request.form.get("hours"))

    conn = sqlite3.connect("planner.db")
    c = conn.cursor()
    c.execute("INSERT INTO subjects (name, hours) VALUES (?, ?)", (name, hours))
    conn.commit()
    conn.close()

    return redirect("/plan")

@app.route("/plan")
def plan():
    conn = sqlite3.connect("planner.db")
    c = conn.cursor()
    c.execute("SELECT * FROM subjects")
    subjects = c.fetchall()
    conn.close()

    total_hours = sum([s[2] for s in subjects]) if subjects else 1
    plan = [(s[1], round((s[2] / total_hours) * 100, 2)) for s in subjects]

    return render_template("plan.html", plan=plan)

if __name__ == "__main__":
    app.run(debug=True)


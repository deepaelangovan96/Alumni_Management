from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# -----------------------------
# Create Database Table
# -----------------------------
def create_table():
    conn = sqlite3.connect("alumni.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alumni(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        batch TEXT,
        department TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()
def create_event_table():
    conn = sqlite3.connect("alumni.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS event_registration(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        event_name TEXT
    )
    """)

    conn.commit()
    conn.close()

create_event_table()

# -----------------------------
# Home
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------
# Register
# -----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        batch = request.form['batch']
        department = request.form['department']

        conn = sqlite3.connect("alumni.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO alumni(name,email,password,batch,department)
        VALUES(?,?,?,?,?)
        """,(name,email,password,batch,department))

        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# -----------------------------
# Login
# -----------------------------
@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("alumni.db")
        cur = conn.cursor()

        cur.execute("""
        SELECT * FROM alumni
        WHERE email=? AND password=?
        """,(email,password))

        user = cur.fetchone()

        conn.close()

        if user:
            return render_template("dashboard.html")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route('/dashboard')
def dashboard():

    conn = sqlite3.connect("alumni.db")
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM alumni")
    total_alumni = cur.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", total_alumni=total_alumni)

# -----------------------------
# View Alumni
# -----------------------------
@app.route('/alumni')
def alumni():

    conn = sqlite3.connect("alumni.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM alumni")

    data = cur.fetchall()

    conn.close()

    return render_template("alumni.html",data=data)

# -----------------------------
# Search Alumni
# -----------------------------
@app.route('/search',methods=['GET','POST'])
def search():

    data=[]

    if request.method=="POST":

        name=request.form['name']

        conn=sqlite3.connect("alumni.db")
        cur=conn.cursor()

        cur.execute("""
        SELECT * FROM alumni
        WHERE name LIKE ?
        """,('%'+name+'%',))

        data=cur.fetchall()

        conn.close()

    return render_template("search.html",data=data)

# -----------------------------
# Edit Alumni
# -----------------------------
@app.route('/edit',methods=['GET','POST'])
def edit():

    if request.method=="POST":

        id=request.form['id']
        name=request.form['name']
        email=request.form['email']
        batch=request.form['batch']
        department=request.form['department']

        conn=sqlite3.connect("alumni.db")
        cur=conn.cursor()

        cur.execute("""
        UPDATE alumni
        SET name=?,email=?,batch=?,department=?
        WHERE id=?
        """,(name,email,batch,department,id))

        conn.commit()
        conn.close()

        return redirect(url_for('alumni'))
    return render_template("edit.html")

# -----------------------------
# Delete Alumni
# -----------------------------
@app.route('/delete',methods=['GET','POST'])
def delete():

    if request.method=="POST":

        id=request.form['id']

        conn=sqlite3.connect("alumni.db")
        cur=conn.cursor()

        cur.execute("""
        DELETE FROM alumni
        WHERE id=?
        """,(id,))

        conn.commit()
        conn.close()

        return redirect(url_for('alumni'))

    return render_template("delete.html")

# -----------------------------
# Events
# -----------------------------
@app.route('/events')
def events():
    return render_template("events.html")

# -----------------------------
# Admin
# -----------------------------
@app.route('/admin')
def admin():
    return render_template("admin.html")
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/event_register/<event_name>', methods=['GET', 'POST'])
def event_register(event_name):

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']

        conn = sqlite3.connect("alumni.db")
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO event_registration(name,email,event_name)
        VALUES(?,?,?)
        """, (name, email, event_name))

        conn.commit()
        conn.close()

        return "<h2>✅ Successfully Registered for " + event_name + "</h2>"

    return render_template("event_register.html", event_name=event_name)
@app.route('/event_registrations')
def event_registrations():

    conn = sqlite3.connect("alumni.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM event_registration")

    data = cur.fetchall()

    conn.close()

    return render_template("event_registrations.html", data=data)

# -----------------------------
# Run Application
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
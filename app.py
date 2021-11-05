from flask import Flask
import flask
import mysql.connector
import db

app = Flask(__name__)
app.debug = True

def mysql_connect():
    # constants right in here
    return mysql.connector.connect(user='root', password = 'password', host='some-mysql')

con = mysql_connect()
db.create_database(con, con.cursor())

@app.route("/")
def index():
    return r"<h1>Flask app :)</h1>"

@app.route("/notes/add/", methods = ["POST"])
def notes_add():
    if (flask.request.method == 'POST'):
        author = flask.request.form('author')
        note = flask.request.form('note')

    con = mysql_connect()
    db.add_note(con, con.cursor(), author, note)
    return flask.redirect(flask.url_for('notes')), 201

@app.route("/notes")
def notes():
    con = mysql_connect()
    all_notes = db.get_all_notes(con, con.cursor())
    return f"<p>{all_notes}</p>"

@app.route("/notes/delete/", methods = ["DELETE"])
def notes_delete():
    id = flask.request.form('del_id')
    con = mysql_connect()
    num_del = db.delete_note_by_id(con, con.cursor(), id)
    return str(num_del), 200

@app.route("notes_temp")
def notes_temp():
    return \
        """<form action="/notes/add" method = "POST">
                <label for="author">Your name: </label>
                <input type="text" id="author" name="author">
                <label for="note">Your note: </label>
                <input type="text" id="note" name="note"> 
                <input type="submit" value="Add note" />

            </form>

            <form action="/notes">
                <input type="submit" value="View notes" />
            </form>

            <form action="/notes/delete method="DELETE">
                <label for="del_id"> ID of note to delete: </label>
                <input type="text" id="del_id" name="del_id">
                <input type="submit" value="Delete note" />
            </form>

        """
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
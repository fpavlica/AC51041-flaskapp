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

@app.route("/notes/add/<author>/<note>", methods = ["POST"])
def notes_add(author, note):
    # if (flask.request.method == 'POST'):
        # author = flask.request.form('author')
        # note = flask.request.form('note')

    con = mysql_connect()
    db.add_note(con, con.cursor(), author, note)
    return flask.redirect(flask.url_for('notes')), 201

@app.route("/notes")
def notes():
    con = mysql_connect()
    all_notes = db.get_all_notes(con, con.cursor())
    return f"<p>{all_notes}</p>"

@app.route("/notes/delete/<id>", methods = ["DELETE"])
def notes_delete(id):
    # id = flask.request.form('')
    con = mysql_connect()
    num_del = db.delete_note_by_id(con, con.cursor(), id)
    return str(num_del), 200
# @app.route("/sql/")
# def sql():
#     cnx = mysql.connector.connect(user='user', password='password',
#                               host='127.0.0.1',
#                               database='testdb')
#     cnx.close()
#     return "sql would be here"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
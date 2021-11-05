# code highly inspired by example provided by Andrew Cobley
# https://github.com/acobley/flaskapp/blob/main/db.py

import mysql.connector

DB_NAME = 'testdb'

TABLES = {}
TABLES['notes'] = \
    """CREATE TABLE if not exists testdb.notes (
        ID int(8) NOT NULL AUTO_INCREMENT,
        author varchar(64) NOT NULL,
        note varchar(255) NOT NULL,
        PRIMARY KEY (ID)
    ) ENGINE=InnoDB"""

def create_database(con, cursor):
    print("creating database")
    cursor.execute("SHOW DATABASES")
    
    # create db itself
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET = 'utf8' ")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)
    print("database created")

    try:
        con.database = DB_NAME
    except mysql.connector.Error as err:
        print(f"Could not set database on connection: {err}")

    print("creating tables")
    for key, value in TABLES:
        print((key, value))
        try:
            cursor.execute(value)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:        
                print("already exists")
            else:
                print(f"Failed to create table: {err}")
        else:
            print("created ok")

    cursor.close()
    con.close() # not exactly sure if it's right to close these here


def add_note(con, cursor, author, note):
    add_note_sql = """INSERT INTO testdb.notes
                        (author, note)
                        VALUES (%s, %s)"""
    cursor.execute(add_note_sql, (author, note))
    con.commit()
    cursor.close()
    con.close()

def get_all_notes(con, cursor):
    get_notes_sql = """SELECT (ID, author, note) FROM testdb.notes"""
    cursor.execute(get_notes_sql)
    result = cursor.fetchall()
    return result

def delete_note_by_id(con, cursor, id):
    sql = """DELETE FROM testdb.notes WHERE ID = %s"""
    cursor.execute(sql, (id,))
    con.commit()
    print(f"{cursor.rowcount} record(s) deleted")
    return cursor.rowcount
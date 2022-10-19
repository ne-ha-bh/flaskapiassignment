import sqlite3

conn = sqlite3.connect("users.sqlite")

cursor =  conn.cursor()
sql_query = """ CREATE TABLE user (
    id integer PRIMARY KEY,
    user_name text NOT NULL
)
"""
cursor.execute(sql_query)

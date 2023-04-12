import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO sharks (sharkname, followers, rating) VALUES (?, ?, ?)",
            ('TS1', 384, 4.6)
            )

cur.execute("INSERT INTO sharks (sharkname, followers, rating) VALUES (?, ?, ?)",
            ('Test Shark 2', 27407, 1.0)
            )

connection.commit()
connection.close()
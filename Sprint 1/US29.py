import sqlite3
import re
dead = []
conn = sqlite3.connect('GEDCOM_DATA.db')
cur = conn.cursor()
cur.execute("SELECT NAME FROM INDIVIDUAL WHERE ALIVE='False'")
rows = cur.fetchall()
for row in rows:
    dead.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(row)))
print("=======================LIST OF DECEASED============================")
for name in dead:
    print(name)






'''
US 35
List all people in a GEDCOM file who were born in the last 30 days

'''
import sqlite3
from datetime import datetime

conn = sqlite3.connect('Sprint4.db')
conn.text_factory = str

query = "SELECT NAME,BIRTHDAY FROM INDIVIDUAL"

date_format = "%d %b %Y"
today = datetime.today().date()

recent_births = []

def main():
    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        
        birth_date = datetime.strptime(row[1],date_format).date()
        difference = today - birth_date

        if difference.days <= 30:
            recent_births.append(row[0].replace("/",""))     # print Name 

    if len(recent_births) > 0:
        print("List of people who were born in the last 30 days")

        for person in recent_births:
            print(person)
    else:
        print("No birth in last 30 days")


main()

def bornRecently(name):

    if name in recent_births:
        return True

    return False
        


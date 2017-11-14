# Developer: Pranit Kulkarni
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('Sprint4.db')
conn.text_factory = str

query = "SELECT MARRIED,DIVORCED,CHILDREN FROM FAMILY"

date_format = "%d %b %Y"

error_tag = "ERROR: US08: "

def formatChildrenData(siblings):
    punctuation = ["{","}",","]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData

def getChildBirthDate(child_id):
    result = conn.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID = ?",(child_id,))
    cursor = result.fetchone()

    if cursor == None:
        return None

    birthdate_text = cursor[0]

    if(birthdate_text != "NA"):
        birthdate = datetime.strptime(birthdate_text,date_format).date()

        return birthdate

    return None

invalid_births = []

def main():
    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        married_date_text = row[0]
        divorce_date_text = row[1]

        parents_marriage_date = None

        if married_date_text != 'NA':
            parents_marriage_date = datetime.strptime(married_date_text,date_format).date()
        
        parents_divorce_date = None

        if divorce_date_text != 'NA':
            parents_divorce_date = datetime.strptime(divorce_date_text,date_format).date()

        children = formatChildrenData(row[2])

        if len(children) > 0:

            for child in children:
                child_birth_date = getChildBirthDate(child)

                if child_birth_date != None and parents_marriage_date != None:

                    if child_birth_date < parents_marriage_date:
                        invalid_births.append(child)
                        print(error_tag+" "+child+" has birthdate before parent's marriage date")
                    elif parents_divorce_date != None:
                        if child_birth_date > parents_divorce_date:
                            difference = child_birth_date - parents_divorce_date

                            months = difference.days/30

                            if months > 9:
                                invalid_births.append(child)
                                print(error_tag+" "+child+" has birthdate 9 months after parent's divorce date")


    if len(invalid_births) == 0:
        print("No invalid births found")


def isBirthInvalid(child_id):

    if child_id in invalid_births:
        return True

    return False



main()  




                


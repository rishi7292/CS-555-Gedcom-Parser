# Developer: Pranit Kulkarni
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('DATA_Sprint3.db')
conn.text_factory = str

query = "SELECT HUSBAND_ID,WIFE_ID FROM FAMILY"

date_format = "%d %b %Y"


def getDeathDate(id):
    #print(id)
    query = "SELECT DEATH FROM INDIVIDUAL WHERE ALIVE = 'False' AND ID = ?",(id,)
    result = conn.execute("SELECT DEATH FROM INDIVIDUAL WHERE ALIVE = 'False' AND ID = ?",(id,))
    row = result.fetchone()

    if row == None:
        return None

    return row[0]

def formatChildrenData(siblings):
    punctuation = ["{","}",","]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData

def getChildBirthDate(id):
    #query = "SELECT BIRTH FROM INDIVIDUAL WHERE ID = "+id
    cursor = conn.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID = ?",(id,))
    result = cursor.fetchone()

    if result == None:
        return None

    birthdate = result[0]

    return birthdate


def calculateDifference(child_birth_date,father_death_date,mother_death_date):
    if child_birth_date != None:
        birthdate = datetime.strptime(child_birth_date,date_format).date()

        if mother_death_date != None:
            deathdate = datetime.strptime(mother_death_date,date_format).date()
            
            if birthdate > deathdate:
                print("ERROR: US09: ")

invalidCases = []

def main():
    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        father_id = row[0]
        mother_id = row[1]

        father_death_date = getDeathDate(father_id)
        mother_death_date = getDeathDate(mother_id)


        #query = "SELECT CHILDREN FROM FAMILY WHERE HUSBAND_ID = "+father_id
        result = conn.execute("SELECT CHILDREN FROM FAMILY WHERE HUSBAND_ID = ?",(father_id,))
        cursor = result.fetchone()
        children = cursor[0]

        childrenList = formatChildrenData(children) 

        if len(childrenList) > 0:
            for child in childrenList:
                child_birth_date = getChildBirthDate(child)

                if child_birth_date != None:
                        birthdate = datetime.strptime(child_birth_date,date_format).date()

                        if mother_death_date != None:
                            deathdate = datetime.strptime(mother_death_date,date_format).date()
                            
                            if birthdate > deathdate:
                                invalidCases.append(child)
                                print("ERROR: US09: "+child+" is born after the death of his mother "+mother_id)

                        if father_death_date != None:
                            deathdate = datetime.strptime(father_death_date,date_format).date()
                            #difference = monthdelta(birthdate,deathdate)    # Gets difference in months..
                            difference = deathdate - birthdate
                            months = difference.days/30

                            if deathdate < birthdate and months > 9:
                                invalidCases.append(child)
                                print("ERROR: US09: "+child+" is born 9 months after the death of his father "+father_id)


def hasInvalidBirth(id):

    if id in invalidCases:
        return True

    return False

main()



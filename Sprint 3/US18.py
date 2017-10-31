# Developer: Pranit Kulkarni
import sqlite3

conn = sqlite3.connect('GEDCOM_DATA_US20.db')
conn.text_factory = str

query = "SELECT HUSBAND_ID,WIFE_ID FROM FAMILY"

def getFamilyId(id):
    query = "SELECT ID FROM FAMILY WHERE CHILDREN LIKE '%"+id+"%' "
    result = conn.execute(query)
    cursor = result.fetchone()
    if(cursor == None):
        return None
    #print("Family ID found: "+cursor[0]+" for "+id)
    return cursor[0]


invalidCases = []
def main():
    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        husband_id = row[0]
        wife_id = row[1]

        husband_family_id = getFamilyId(husband_id)
        wife_family_id = getFamilyId(wife_id)

        if(husband_family_id == wife_family_id and husband_family_id != None):
            print("ERROR: US08: "+husband_id+" and "+wife_id+" who are married are siblings")
            invalidCases.append(husband_id)
            invalidCases.append(wife_id)


def isMarriedToASibbling(id):

    if id in invalidCases:
        return True

    return False


main()


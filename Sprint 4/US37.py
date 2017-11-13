'''
US37 : List all living spouses and descendants of people in a GEDCOM file 
who died in the last 30 days

@Author : Shreyas Sule
'''
import sqlite3
import US36

conn = sqlite3.connect("Sprint4.db")
conn.text_factory = str


recent_deaths = US36.deaths()

def formatChildrenData(siblings):
    punctuation = ["{","}",",","(",")"]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData

def recent_survivors():
    
    for id in recent_deaths:

        #if the id has no spouse
        validation_query = conn.execute("SELECT SPOUSE FROM INDIVIDUAL WHERE ID = ?",(id,))
        validation_query_result = validation_query.fetchone()
        if(validation_query_result == 'NA'):
            print(id+" was single")
        else:
            query2 = conn.execute("SELECT HUSBAND_ID,WIFE_ID,CHILDREN from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL WHERE ID = ?)",(id,))
            query2_result = query2.fetchall()
            
            for data in query2_result:
                husband_id = data[0]
                wife_id = data[1]
                children = data[2]

                children = formatChildrenData(children)
                child_str = ""
                for child_id in children:
                    child_str += child_id+" "
                if(id == husband_id):
                    print(id+" died in last 30 days and was the husband of  "+wife_id+" and had "+child_str+" as their children")
                elif(id == wife_id):
                    print(id+" died in last 30 days and was the wife of "+husband_id+" and had "+child_str+"as their children ")


def deadRecently(id):

    if id in recent_deaths:
        return True

    return False

recent_survivors()
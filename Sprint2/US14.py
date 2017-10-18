import sqlite3
import datetime
import Family

conn = sqlite3.connect("GEDCOM_DATA_US14.db")
conn.text_factory = str

query = "SELECT ID,CHILDREN from FAMILY"

result = conn.execute(query)
data = result.fetchall()



def formatChildrenData(siblings):
    punctuation = ["{","}",","]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData


def us14MultipleSiblings():

    for familyData in data:
        famId = familyData[0]
        children = familyData[1]

        siblings = formatChildrenData(children)

        noOfSiblings = len(siblings)

        if(noOfSiblings >= 5):
            famObj = Family.Family()
            famObj.setFamId(famId)

            for indi_id in siblings:
                birth_date_query = conn.execute("SELECT BIRTHDAY from INDIVIDUAL where ID = ?",(indi_id,))
                birthdates = birth_date_query.fetchall()

                for dates in birthdates:
                    myBirthDate = datetime.datetime.strptime(dates[0],'%d %b %Y').date()
                    famObj.setBirthdate(myBirthDate)
            
            checkSiblings = famObj.validateNoOfSiblings()
            if(checkSiblings):
                print(famObj.getFamId()+" has "+str(noOfSiblings)+" siblings "+",".join(siblings)+" born on the same day")


def noOfSiblings(id):

    children = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(id,))
    children = children.fetchall()
    for row in children:
        siblings = formatChildrenData(row[0])

    return len(siblings)
 




us14MultipleSiblings()




        
        
        

            
            
            

        
        
    
        
        


#print(childrenData)





    
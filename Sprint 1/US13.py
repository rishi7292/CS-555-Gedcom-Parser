import sqlite3
import datetime

conn = sqlite3.connect("GEDCOM_DATA.db")
conn.text_factory = str

sql = "SELECT ID,CHILDREN from FAMILY"

result = conn.execute(sql)

data = result.fetchall()

punctuation = ["{","}",","]



myData = {}
#print myData

for row in data:
    id = row[0]
    children = row[1]
    for c in punctuation:
        children = children.replace(c," ").strip()
    childrenData = children.split(" ")
    myData[id] = childrenData


for key,value in myData.items():
    flag = True
    siblingDates = []
    for childId in value:
        query = conn.execute("SELECT BIRTHDAY from INDIVIDUAL  where ID = ?",(childId,))
        rows = query.fetchall()
        for birthdate in rows:
            siblingDates.append(birthdate[0])

    temp1 = -1
    temp2 = -1
    for i in range(len(siblingDates)):
        for j in range(i+1,len(siblingDates)):
            child1 = datetime.datetime.strptime(siblingDates[i],'%d %b %Y').date()
            yearOfChild1 = child1.year
            monthOfChild1 = child1.month
            dayOfChild1 = child1.day

            child2 = datetime.datetime.strptime(siblingDates[j],'%d %b %Y').date()
            yearOfChild2 = child2.year
            monthOfChild2 = child2.month
            dayOfChild2 = child2.day

            if((yearOfChild2 - yearOfChild1) < 1):
                if((monthOfChild2 - monthOfChild1) < 8 or (dayOfChild2 - dayOfChild1) < 2 ):
                    flag = False
                    temp1 = i
                    temp2 = j
                    break
    if(flag == False):
        print(value[temp1]+" and "+value[temp2]+" from "+key+" have invalid spacing")
        




        
    



    



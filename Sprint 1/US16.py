import sqlite3

conn = sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str

query = "SELECT ID,HUSBAND_NAME,CHILDREN FROM FAMILY"

result = conn.execute(query)
rows = result.fetchall()


for row in rows:
    family_id = row[0]
    last_name = (row[1].replace("/","").split(" "))[1]
    #print(last_name)

    isLastNameSame = True
    children = row[2]
    children = children.replace("{","")
    children = children.replace("}","")

    childIds = children.split(",")
    for childId in childIds:

        result1 = conn.execute("SELECT NAME FROM INDIVIDUAL WHERE ID = ? and GENDER = ?",(childId,"M"))
        db_rows = result1.fetchall()

        for son_name in db_rows:
            names = son_name[0].replace("/","").split(" ")
            son_last_name = names[1]

            if(last_name != son_last_name):
                isLastNameSame = False
                break

        
    if(isLastNameSame == False):
        print(names[0]+" "+names[1]+" does not have the same family name "+last_name)
        #print("All the male members in family "+family_id+" do not have the same last name")


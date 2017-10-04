import sqlite3
import datetime
import re
import pandas as pd
conn = sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str
indi_table=pd.read_sql_query('SELECT * FROM INDIVIDUAL', conn)
fam_table=pd.read_sql_query('SELECT * FROM FAMILY', conn)
print('INDIVIDUAL TABLE')
print(indi_table)
print('FAMILY TABLE')
print(fam_table)
# Pranit Kulkarni
def US16():
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
            print("ERROR: "+" US16: "+names[0]+" "+names[1]+" does not have the same family name "+last_name)


# Pranit Kulkarni
def US21():
    query1 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT HUSBAND_ID FROM FAMILY)"
    result1 = conn.execute(query1)

    husbands = result1.fetchall()

    for row in husbands:
        if row[1] != "M":
            name = row[0].replace("/","")
            print("ERROR: "+" US21: "+"Husband "+name+" is not Male")


    query2 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT WIFE_ID FROM FAMILY)"

    result2 = conn.execute(query2)

    wives = result2.fetchall()

    for row in wives:
        
        if row[1] != "F":
            name = row[0].replace("/","")
            print("ERROR: "+" US21: "+"Wife "+name+" is not female")
    


def US13():     # SIBLING SPACING  BY SHREYAS SULE
    sql = "SELECT ID,CHILDREN from FAMILY"

    result = conn.execute(sql)
    data = result.fetchall()

    punctuation = ["{","}",","]

    myData = {}

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
            print("ERROR: "+" US13: "+value[temp1]+" and "+value[temp2]+" from "+key+" have invalid spacing")

def US22():
    error_tag = "ERROR: "+" US22: "
    query1 = "SELECT ID from INDIVIDUAL"
    query2 = "SELECT ID from FAMILY"

    result1 = conn.execute(query1)
    result2 = conn.execute(query2)

    all_INDI_IDs = result1.fetchall()
    all_FAM_IDs = result2.fetchall()

    INDI_ID = []
    FAM_ID = []


    for ID in all_INDI_IDs:
        INDI_ID.append(ID[0])

    for i in range(len(INDI_ID)):
        for j in range(i+1,len(INDI_ID)):
            if INDI_ID[i] == INDI_ID[j]:
                print(error_tag+INDI_ID[i]+" is not unique")

    for ID in all_FAM_IDs:
        FAM_ID.append(ID[0])


    for i in range(len(FAM_ID)):
        for j in range(i+1,len(FAM_ID)):
            if FAM_ID[i] == FAM_ID[j]:
                print(error_tag+FAM_ID[i]+" is not unique")
    




def US25():
    error_tag = "ERROR: "+" US25: "
    flag = 0
    c = []
    fam_id = []
    children_id = []
    name = []
    bday = []
    #conn = sqlite3.connect('GEDCOM_DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT ID, CHILDREN FROM FAMILY")
    rows = cur.fetchall()

    for fid, chid in rows:
        fam_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(fid)))
        children_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(chid)))

    for i, id in enumerate(fam_id):
        c= children_id[i].split(',')
        for j in c:
            if j == 'NA':
                flag = 1
            else:
                cur.execute("SELECT NAME, BIRTHDAY FROM INDIVIDUAL WHERE ID=?",(j,))
                irows = cur.fetchall()
                for nm,bd in irows:
                    name.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(nm)))
                    bday.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(bd)))
        if flag == 1:
            print(error_tag+"The family id "+ id+ " has no child")
            flag = 0
        else:
            if len(name) != len(set(name)) and len(bday) != len(set(bday)):
                print(error_tag+"The children of family id "+ id +" does not have unique first names!")
            #else:
               # print(error_tag+"The children of family id "+ id+ " has unique first names!")


def US29():
    dead = []
    #conn = sqlite3.connect('GEDCOM_DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT NAME FROM INDIVIDUAL WHERE ALIVE='False'")
    rows = cur.fetchall()
    for row in rows:
        dead.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(row)))
    #print("=======================LIST OF DECEASED============================")
    for name in dead:
        print("US29: "+name+" is dead")
        #print(name)


def US03():
    query1="select NAME,AGE from INDIVIDUAL"

    result1=conn.execute(query1)

    value=result1.fetchall()
    first=value[0]

    for row in value:
        if(row[1]<=0):
            print ("ERROR: US03: "+row[0].replace("/"," ")+"has an invalid age since birthday is after death day")


def US02():
    query1="select NAME,BIRTHDAY,MARRIED from INDIVIDUAL AS I,FAMILY AS F where I.ID=F.HUSBAND_ID OR I.ID=F.WIFE_ID"  

    result1=conn.execute(query1)

    value=result1.fetchall()
    first=value[0]

    i=0
    for row in value:
        first_row=value[i]
        a=datetime.datetime.strptime(first_row[1],'%d %b %Y')
        a.strftime('%d %m %Y')
    
        b=datetime.datetime.strptime(first_row[2],'%d %b %Y')
        a.strftime('%d %m %Y')
        i+=1
  #  print (first_row)
        if(a > b):
            print ("ERROR: US02: "+first_row[0].replace("/"," ")+" is born after their own marriage which is not possible ")


# User stories by Pranit
US16()
US21()

# User stories by Shreyas
US13()
US22()

# User stories by Aakanksha
US25()
US29()

# User stories by Rishi
US03()
US02()

conn.close()
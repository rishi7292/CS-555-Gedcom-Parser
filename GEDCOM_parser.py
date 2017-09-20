import sqlite3
from datetime import date, datetime
import pandas as pd

birth = 0
death = 0
chld = []
tag_name = {}

output_file = open(r'./output_file','a+')

def cal_age(bd, dd):
    today = date.today()
    if dd == 0:
        obj.age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    else:
        obj.age = dd.year - bd.year - ((dd.month, dd.day) < (bd.month, bd.day))


conn = sqlite3.connect('GEDCOM_DATA.db')
print('Database connection made')

conn.execute(
    " CREATE TABLE IF NOT EXISTS INDIVIDUAL ( ID TEXT PRIMARY KEY NOT NULL, NAME TEXT, GENDER TEXT, BIRTHDAY TEXT, AGE INT, ALIVE TEXT, DEATH TEXT, CHILD TEXT, SPOUSE TEXT ) ")
conn.execute(
    " CREATE TABLE IF NOT EXISTS FAMILY (ID TEXT PRIMARY KEY NOT NULL, MARRIED TEXT, DIVORCED TEXT, HUSBAND_ID TEXT, HUSBAND_NAME TEXT, WIFE_ID TEXT, WIFE_NAME TEXT, CHILDREN TEXT)")
print('Table created')

cur = conn.cursor()
name = 'NAME'
table_nm = 'INDIVIDUAL'
col_nm = 'ID'


class Individual:
    id = ""
    name = "NA"
    sex = "NA"
    birth = "NA"
    age = ""
    alive = "True"
    death = "NA"
    child_id = "NA"
    spouse_id = "NA"


class Family:
    id = ""
    marriage_date = "NA"
    divorce = "NA"
    husband_id = "NA"
    husband_name = "NA"
    wife_id = "NA"
    wife_name = "NA"
    children = "NA"


obj = Individual()  # Initialize to make it global...

myfile = open("FAMILY1.ged")
lines = myfile.readlines()
myfile.close

validTags0 = ['HEAD', 'TRLR', 'NOTE']
# validTags1 = ['NAME','SEX','BIRT','DEAT','FAMC','FAMS','MARR','HUSB','WIFE','CHIL','DIV']
tagsForIndi = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']  # tags that should be in level 1 for INDI
tagsForFam = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', '_CURRENT']  # tags that should be in level 1 for FAM

canInsert = False
flag = 0
tag1 = ""
temp = 0

# print("Lines "+lines)

for line in lines:
    words = line.strip().split(" ")  # strip removes unnecessary spaces..
    level = words[0]
    #print("Level parsing -> " + level)

    if level == '0':

        isValid = False
        isIndi = False
        isFam = False

        if 'INDI' in line and words[2] == 'INDI':  # Check if the line has INDI
            isIndi = True
            isValid = True
        elif 'FAM' in line and words[2] == 'FAM':
            isFam = True
            isValid = True
        elif 'TRLR' in line and words[1] == 'TRLR':
            isValid = True

        '''print("LEVEL 0")
        print("canInsert "+canInsert)
        print("flag "+flag)
        print("isValid "+isValid)'''

        if isValid:

            if canInsert:  # Skip for the first time..so every time you end up with all the data for LEVEL 0 insert it in the table
                # insert(obj,flag)... call function to Insert the previous INDI or FAM obj in database accordingly
                if flag == 1:
                    conn.execute("""INSERT INTO INDIVIDUAL VALUES (?,?,?,?,?,?,?,?,?);""", (
                    obj.id, obj.name, obj.sex, obj.birth, obj.age, obj.alive, obj.death, obj.child_id, obj.spouse_id))
                    conn.commit()
                elif flag == 2:
                    conn.execute("""INSERT INTO FAMILY VALUES (?,?,?,?,?,?,?,?);""", (
                    obj.id, obj.marriage_date, obj.divorce, obj.husband_id, obj.husband_name, obj.wife_id,
                    obj.wife_name, obj.children))
                    conn.commit()

            if isIndi:
                obj = Individual()
                obj.id = words[1]
                canInsert = True
                flag = 1

            if isFam:
                obj = Family()
                obj.id = words[1]
                canInsert = True
                flag = 2

    if level == '1':
        tag1 = words[1]

        if tag1 in tagsForIndi:

            arguments = " ".join(words[2:])

            if tag1 == tagsForIndi[0]:
                obj.name = arguments
                tag_name[obj.id] = arguments
            elif tag1 == tagsForIndi[1]:
                obj.sex = arguments
            elif tag1 == tagsForIndi[2]:
                temp = 1  # Get the date in next line from LEVEL 2
            elif tag1 == tagsForIndi[3]:
                temp = 1  # Get the date in next line from LEVEL 2
                if words[2] == 'Y':
                    obj.alive = "False"
            elif tag1 == tagsForIndi[4]:
                obj.child_id = arguments
            elif tag1 == tagsForIndi[5]:
                obj.spouse_id = arguments


        elif tag1 in tagsForFam:  # .. similar tags checking and adding to the fam obj

            arguments = " ".join(words[2:])

            if tag1 == tagsForFam[0]:
                temp = 2  # Get the date in next line from LEVEL 2
            elif tag1 == tagsForFam[1]:
                obj.husband_id = arguments
                obj.husband_name = tag_name[arguments]
            elif tag1 == tagsForFam[2]:
                obj.wife_id = arguments
                obj.wife_name = tag_name[arguments]
            elif tag1 == tagsForFam[3]:
                chld.append(arguments)
            elif tag1 == tagsForFam[4]:
                temp = 2  # Get the date in next line from LEVEL 2
            elif tag1 == tagsForFam[5]:
                if not chld:
                    obj.children = "NA"
                else:
                    obj.children = '{' + ','.join(chld) + '}'
                chld = []

    if level == '2':

        if words[1] == 'DATE':

            dateArgument = " ".join(words[2:])

            # Find which date it is & assign it to the object's variable accordingly

            if temp == 1:  # INDI
                if tag1 == tagsForIndi[2]:
                    obj.birth = dateArgument
                    birth = datetime.strptime(dateArgument, '%d %b %Y')
                elif tag1 == tagsForIndi[3]:
                    obj.death = dateArgument
                    death = datetime.strptime(dateArgument, '%d %b %Y')
                # Calculating age
                cal_age(birth, death)
                death = 0

            if temp == 2:
                if tag1 == tagsForFam[0]:
                    obj.marriage_date = dateArgument
                elif tag1 == tagsForFam[1]:
                    obj.divorce = dateArgument

#print(tag_name)

indi_table=pd.read_sql_query('SELECT * FROM INDIVIDUAL', conn)
fam_table=pd.read_sql_query('SELECT * FROM FAMILY', conn)
print('INDIVIDUAL TABLE')
print(indi_table)
print('FAMILY TABLE')
print(fam_table)
output_file.write('INDIVIDUAL TABLE\n')
output_file.write(str(indi_table))
output_file.write('\n\nFAMILY TABLE\n')
output_file.write(str(fam_table))

output_file.close()
conn.close()
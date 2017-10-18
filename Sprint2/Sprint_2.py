import sqlite3
from _datetime import datetime
import re
import Family
import pandas as pd
import GEDCOM_parser

conn = sqlite3.connect('DATA.db')
conn.text_factory = str

indi_table = pd.read_sql_query('SELECT * FROM INDIVIDUAL', conn)
fam_table = pd.read_sql_query('SELECT * FROM FAMILY', conn)
print('INDIVIDUAL TABLE')
print(indi_table)
print('FAMILY TABLE')
print(fam_table)

#Shreyas Sule
def US19():
    result = conn.execute("SELECT ID,CHILDREN from FAMILY")
    data = result.fetchall()
    chk = []

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ",", "(", ")"]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData

    def us19FirstCousins():

        for familyData in data:
            famId = familyData[0]
            children = familyData[1]

            siblings = formatChildrenData(children)
            # print(siblings)
            if (len(siblings) >= 1):
                for indi_id in siblings:
                    flag = 0
                    # Get parents of current child
                    parent_query = conn.execute(
                        "SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT CHILD from INDIVIDUAL where ID = ?)",
                        (indi_id,))
                    parents = parent_query.fetchone()
                    # print(parents)
                    # parents = list(parents)
                    # print(parents)
                    cousins = []
                    parents_siblings = []
                    if (parents != None):
                        father = parents[0]
                        # print(father)
                        mother = parents[1]

                        father_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?", (father,))
                        father_family = father_family_query.fetchall()
                        father_family = [i[0] for i in father_family]
                        # print(father_family)

                        if (father_family[0] != 'NA'):

                            for fatherId in father_family:
                                siblingsOfFatherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",
                                                                     (fatherId,))
                                siblingsOfFather = siblingsOfFatherQuery.fetchall()
                                siblingsOfFather = [i[0] for i in siblingsOfFather]
                                siblingsOfFather = re.sub(r'[^@I0-9,]', '', siblingsOfFather[0])
                                siblingsOfFather = siblingsOfFather.split(",")
                                # print(siblingsOfFather)
                                # Store all siblings of father except father himself.
                                for siblingId in siblingsOfFather:
                                    if (siblingId != fatherId):
                                        parents_siblings.append(siblingId)
                        # print(parents_siblings)


                        mother_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?", (mother,))
                        mother_family = mother_family_query.fetchall()
                        mother_family = [i[0] for i in mother_family]

                        if (mother_family[0] != 'NA'):

                            for motherId in mother_family:
                                siblingsOfMotherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",
                                                                     (motherId,))
                                siblingsOfMother = siblingsOfMotherQuery.fetchall()
                                siblingsOfMother = [i[0] for i in siblingsOfMother]
                                siblingsOfMother = re.sub(r'[^@I0-9,]', '', siblingsOfMother[0])
                                siblingsOfMother = siblingsOfMother.split(",")

                                # print(siblingsOfMother)

                                # Store all siblings of father except father himself.
                                for siblingId in siblingsOfMother:
                                    if (siblingId != motherId):
                                        parents_siblings.append(siblingId)

                                        # print(parent_siblings+" all siblings ")

                        # print(parents_siblings)

                        for parentSiblingIds in parents_siblings:

                            """
                            parentSiblingIds = list(parentSiblingIds)
                            parentSiblingIds = re.sub(r'[^@I0-9,]','',parentSiblingIds[0])
                            parentSiblingIds = parentSiblingIds.split(',')
                            """
                            # print(parentSiblingIds)


                            cousinFamilyQuery = conn.execute("SELECT SPOUSE from INDIVIDUAL where ID = ?",
                                                             (parentSiblingIds,))

                            cousinFamilyId = cousinFamilyQuery.fetchall()
                            cousinFamilyId = [i[0] for i in cousinFamilyId]
                            # print(cousinFamilyId)

                            for cId in cousinFamilyId:

                                if (cousinFamilyId != None):

                                    cousinsQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?", (cId,))
                                    cousinData = cousinsQuery.fetchone()
                                    if (cousinData != None):

                                        cousinData = list(cousinData)
                                        cousinData = re.sub(r'[^@I0-9,]', '', cousinData[0])
                                        cousinData = cousinData.split(',')
                                        for i in cousinData:
                                            cousins.append(i)
                                        # print(cousins)

                                        for id in cousins:
                                            mySpouseQuery = conn.execute(
                                                "SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL where ID = ?)",
                                                (id,))
                                            mySpouse = mySpouseQuery.fetchone()
                                            if (mySpouse != None):
                                                mySpouse = list(mySpouse)
                                                husband = mySpouse[0]
                                                wife = mySpouse[1]
                                                # print(husband,wife)
                                        if husband in cousins and wife in cousins:
                                            if husband in chk and wife in chk:
                                                flag = 1
                                                return flag,1
                                                #h = husband
                                                #w = wife
                                                #flag = 1
                                            else:
                                                flag = 0
                                                chk.append(husband)
                                                chk.append(wife)
                                                return chk,flag,0
            #if (flag == 1):
                # flag1 = 1
                #print("ERROR: US19: ID-", h, " and ", w, "are first cousins and married")

    chk1,f,x = us19FirstCousins()
    if(f==0 and x==0):
        ids1 = ",".join(chk1)
        print("ERROR: US19: IDs-",ids1," are First cousins and married!")


# Pranit Kulkarni
def US16():
    query = "SELECT ID,HUSBAND_NAME,CHILDREN FROM FAMILY"

    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        family_id = row[0]
        last_name = (row[1].replace("/", "").split(" "))[1]
        # print(last_name)

        isLastNameSame = True
        children = row[2]
        children = children.replace("{", "")
        children = children.replace("}", "")

        childIds = children.split(",")
        for childId in childIds:

            result1 = conn.execute("SELECT NAME FROM INDIVIDUAL WHERE ID = ? and GENDER = ?", (childId, "M"))
            db_rows = result1.fetchall()

            for son_name in db_rows:
                names = son_name[0].replace("/", "").split(" ")
                son_last_name = names[1]

                if (last_name != son_last_name):
                    isLastNameSame = False
                    break

        if (isLastNameSame == False):
            print(
                "ERROR: " + " US16: " + names[0] + " " + names[1] + " does not have the same family name " + last_name)


# Pranit Kulkarni
def US21():
    query1 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT HUSBAND_ID FROM FAMILY)"
    result1 = conn.execute(query1)

    husbands = result1.fetchall()

    for row in husbands:
        if row[1] != "M":
            name = row[0].replace("/", "")
            print("ERROR: " + " US21: " + "Husband " + name + " is not Male")

    query2 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT WIFE_ID FROM FAMILY)"

    result2 = conn.execute(query2)

    wives = result2.fetchall()

    for row in wives:

        if row[1] != "F":
            name = row[0].replace("/", "")
            print("ERROR: " + " US21: " + "Wife " + name + " is not female")


def US13():  # SIBLING SPACING  BY SHREYAS SULE
    sql = "SELECT ID,CHILDREN from FAMILY"

    result = conn.execute(sql)
    data = result.fetchall()

    punctuation = ["{", "}", ","]

    myData = {}


    for row in data:
        id = row[0]
        children = row[1]
        for c in punctuation:
            children = children.replace(c, " ").strip()
        childrenData = children.split(" ")
        myData[id] = childrenData

    for key, value in myData.items():
        flag = True
        siblingDates = []
        Invalid_siblings = []
        for childId in value:
            query = conn.execute("SELECT BIRTHDAY from INDIVIDUAL  where ID = ?", (childId,))
            rows = query.fetchall()
            for birthdate in rows:
                siblingDates.append(birthdate[0])

        temp1 = -1
        temp2 = -1
        for i in range(len(siblingDates)):
            for j in range(i + 1, len(siblingDates)):
                child1 = datetime.strptime(siblingDates[i], '%d %b %Y').date()
                yearOfChild1 = child1.year
                monthOfChild1 = child1.month
                dayOfChild1 = child1.day

                child2 = datetime.strptime(siblingDates[j], '%d %b %Y').date()
                yearOfChild2 = child2.year
                monthOfChild2 = child2.month
                dayOfChild2 = child2.day

                if ((yearOfChild2 - yearOfChild1) < 1):
                    if ((monthOfChild2 - monthOfChild1) < 8 or (dayOfChild2 - dayOfChild1) < 2):
                        flag = False
                        temp1 = i
                        temp2 = j
                        if value[temp1] not in Invalid_siblings:
                            Invalid_siblings.append(value[temp1])
                        if value[temp2] not in Invalid_siblings:
                            Invalid_siblings.append(value[temp2])
                        break

        if (flag == False):
            invalid_id_str = ",".join(Invalid_siblings)
            print("ERROR: US13: " + invalid_id_str +" from " + key + " have invalid spacing")


def US22():
    '''
    error_tag = "ERROR: " + " US22: "
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
        for j in range(i + 1, len(INDI_ID)):
            if INDI_ID[i] == INDI_ID[j]:
                print(error_tag + INDI_ID[i] + " is not unique")

    for ID in all_FAM_IDs:
        FAM_ID.append(ID[0])

    for i in range(len(FAM_ID)):
        for j in range(i + 1, len(FAM_ID)):
            if FAM_ID[i] == FAM_ID[j]:
                print(error_tag + FAM_ID[i] + " is not unique")
###################### NOTE AHEAD #######################################
Adding a duplicate ID in GEDCOM File will stop the execution of creating a table in the intermediate stage, so
for the time being we created an erronous GEDCOM file and parsed it for the purpose of notifying the customer of
Duplicate ID case.
'''
    try:
        GEDCOM_parser.parse('FamilyTree1.ged')
    except:
        print("ERROR: US22: Duplicate IDs found in the GEDCOM")

def US25():
    error_tag = "ERROR: " + " US25: "
    flag = 0
    c = []
    fam_id = []
    children_id = []
    name = []
    bday = []
    # conn = sqlite3.connect('GEDCOM_DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT ID, CHILDREN FROM FAMILY")
    rows = cur.fetchall()

    for fid, chid in rows:
        fam_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(fid)))
        children_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(chid)))

    for i, id in enumerate(fam_id):
        c = children_id[i].split(',')
        for j in c:
            if j == 'NA':
                flag = 1
            else:
                cur.execute("SELECT NAME, BIRTHDAY FROM INDIVIDUAL WHERE ID=?", (j,))
                irows = cur.fetchall()
                for nm, bd in irows:
                    name.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(nm)))
                    bday.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(bd)))
        if flag == 1:
            print(error_tag + "The family id " + id + " has no child")
        else:
            if len(name) != len(set(name)) and len(bday) != len(set(bday)):
                print(error_tag + "The children of family id " + id + " does not have unique first names!")
                # else:
                # print(error_tag+"The children of family id "+ id+ " has unique first names!")


def US29():
    dead = []
    # conn = sqlite3.connect('GEDCOM_DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT NAME FROM INDIVIDUAL WHERE ALIVE='False'")
    rows = cur.fetchall()
    for row in rows:
        dead.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(row)))
    # print("=======================LIST OF DECEASED============================")
    for name in dead:
        print("US29: " + name + " is dead")
        # print(name)


def US03():
    query1 = "select NAME,AGE from INDIVIDUAL"

    result1 = conn.execute(query1)

    value = result1.fetchall()
    first = value[0]

    for row in value:
        if (row[1] <= 0):
            print("ERROR: US03: " + row[0].replace("/", " ") + "has an invalid age since birthday is after death day")


def US02():
    query1 = "select NAME,BIRTHDAY,MARRIED from INDIVIDUAL AS I,FAMILY AS F where I.ID=F.HUSBAND_ID OR I.ID=F.WIFE_ID"

    result1 = conn.execute(query1)

    value = result1.fetchall()
    first = value[0]

    i = 0
    a = ''
    b = ''
    for row in value:
        first_row = value[i]
        if(first_row[1]!='NA' and first_row[2]!='NA'):
            a = datetime.strptime(first_row[1], '%d %b %Y')
            a.strftime('%d %m %Y')

            b = datetime.strptime(first_row[2], '%d %b %Y')
            a.strftime('%d %m %Y')
        i += 1
        #  print (first_row)
        if (a > b):
            print("ERROR: US02: " + first_row[0].replace("/",
                                                         " ") + " is born after their own marriage which is not possible ")


def US11():
    HID = []
    WID = []
    HName = []
    WName = []
    div_date = []
    marr_date = []
    SP_ID = []
    check_list = []
    #conn = sqlite3.connect('DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT SPOUSE FROM INDIVIDUAL WHERE LENGTH(SPOUSE)>5")
    rows = cur.fetchall()
    for spid in rows:
        SP_ID = list(spid)
        SP_ID = SP_ID[0].split(',')
    for spid in SP_ID:
        cur.execute("SELECT MARRIED,DIVORCED,HUSBAND_ID,HUSBAND_NAME,WIFE_ID,WIFE_NAME FROM FAMILY WHERE ID=?", (spid,))
        rows1 = cur.fetchall()
        for m, d, hid, hnm, wid, wnm in rows1:
            marr_date.append(re.sub(r'[^0-9a-zA-Z ]', '', str(m)))
            div_date.append(re.sub(r'[^0-9a-zA-Z ]', '', str(d)))
            HID.append(re.sub(r'[^@0-9a-zA-Z ]', '', str(hid)))
            HName.append(re.sub(r'[^0-9a-zA-Z ]', '', str(hnm)))
            WID.append(re.sub(r'[^@0-9a-zA-Z]', '', str(wid)))
            WName.append(re.sub(r'[^0-9a-zA-Z ]', '', str(wnm)))
    if len(HID) != len(set(HID)):
        for p, id in enumerate(set(HID)):
            div = div_date[p]
            if div != "NA":
                # do something when there is divorce date for the individual
                print(div)
                mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
                mdt1 = datetime.date(mdt1)
                mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
                mdt2 = datetime.date(mdt2)
                div = datetime.strptime(str(div), "%d %b %Y")
                div = datetime.date(div)
                if mdt1 < mdt2:
                    end = mdt2
                    start = mdt1
                else:
                    end = mdt1
                    start = mdt2
                if start < div < end:
                    continue
                else:
                    check_list.append(id)
                    print("ERROR: US11: ID-", id, "is in a bigamous relationship!")
            else:
                mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
                mdt1 = datetime.date(mdt1)
                mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
                mdt2 = datetime.date(mdt2)
                if mdt1 < mdt2:
                    pos = p
                    end = mdt2
                    start = mdt1
                else:
                    pos = p + 1
                    end = mdt1
                    start = mdt2
                cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?", (WID[pos],))
                rr = cur.fetchall()
                for d in rr:
                    d = re.sub(r'[^0-9a-zA-Z ]', '', str(d))
                    if d != "NA":
                        d = datetime.strptime(str(d), "%d %b %Y")
                        d = datetime.date(d)
                        if start < d < end:
                            continue
                        else:
                            check_list.append(id)
                            print("ERROR: US11: ID-", id, "has bigamous relationship!")
                    else:
                        print("ERROR: Insufficient data - The individual", id,
                              " may or may not have a bigamous relationship")
    if len(WID) != len(set(WID)):
        for p, id in enumerate(set(WID)):
            div = div_date[p]
            if div != "NA":
                print(div)
                # do something when there is divorce date for the individual
                mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
                mdt1 = datetime.date(mdt1)
                mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
                mdt2 = datetime.date(mdt2)
                div = datetime.strptime(str(div), "%d %b %Y")
                div = datetime.date(div)
                if mdt1 < mdt2:
                    end = mdt2
                    start = mdt1
                else:
                    end = mdt1
                    start = mdt2
                if start < div < end:
                    continue
                else:
                    check_list.append(id)
                    print("ERROR: US11: ID-", id, "is in a bigamous relationship!")
            else:
                mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
                mdt1 = datetime.date(mdt1)
                mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
                mdt2 = datetime.date(mdt2)
                if mdt1 < mdt2:
                    pos = p
                    end = mdt2
                    start = mdt1
                else:
                    pos = p + 1
                    end = mdt1
                    start = mdt2
                cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?", (HID[pos],))
                rr = cur.fetchall()
                for d in rr:
                    d = re.sub(r'[^0-9a-zA-Z ]', '', str(d))
                    if d != "NA":
                        d = datetime.strptime(str(d), "%d %b %Y")
                        d = datetime.date(d)
                        if start < d < end:
                            continue
                            print("No individual is in a bigamous relationship!")
                        else:
                            check_list.append(id)
                            print("ERROR: US11: ID-", id, "has bigamous relationship!")
                    else:
                        print("ERROR: Insufficient data - The individual", id,
                              "may or may not have a bigamous relationship")


def US10():
    def age_at_marriage(d1, d2):
        if d1=='NA' or d2=='NA':
            return -1
        else:
            age = 0
            d1 = datetime.strptime(d1, "%d %b %Y")
            d2 = datetime.strptime(d2, "%d %b %Y")
            age = d2.year - d1.year - ((d2.month, d2.day) < (d1.month, d1.day))
            return age
    husb_id =[]
    husb_bd = []
    wife_id = []
    wife_bd = []
    marr_date = []
    under_age = []
    #conn = sqlite3.connect('GEDCOM_DATA14-2.db')
    cur = conn.cursor()
    cur.execute("SELECT HUSBAND_ID, WIFE_ID, MARRIED FROM FAMILY")
    rows = cur.fetchall()
    for husbid,wifeid,mardt in rows:
        husb_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(husbid)))
        wife_id.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(wifeid)))
        marr_date.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(mardt)))
    for hid in husb_id:
        cur.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID=?",(hid,))
        rows1 = cur.fetchall()
        husb_bd.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(rows1)))
    for wid in wife_id:
        cur.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID=?",(wid,))
        rows2 = cur.fetchall()
        wife_bd.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(rows2)))
    for hid,hmdt,hbdt in zip(husb_id,marr_date,husb_bd):
        age = age_at_marriage(hbdt,hmdt)
        if age < 14 and age>=0:
            under_age.append(hid)
            print("ERROR: US10: ",hid," is under 14 years of age when he was married")
    for wid,wmdt,wbdt in zip(wife_id,marr_date,wife_bd):
        age = age_at_marriage(wbdt,wmdt)
        if age < 14 and age>=0:
            under_age.append(wid)
            print("ERROR: US10: ",wid," is under 14 years of age when she was married")

def US07():
    query = "SELECT NAME,ALIVE,AGE,BIRTHDAY,DEATH FROM INDIVIDUAL"

    error_tag = "ERROR: US07: "
    result = conn.execute(query)
    rows = result.fetchall()

    date_format = "%d %b %Y"
    today = datetime.today().date()

    for row in rows:
        name = row[0].replace("/", "")

        if row[1] == "False":
            age = row[2]

            if (age > 150):
                print(error_tag + name + " who is dead does not have valid age")

        elif row[1] == "True":
            birthdateText = row[3]

            birthdate = datetime.strptime(birthdateText, date_format).date()
            difference = today - birthdate

            years = difference.days / 365

            if years >= 150:
                print(error_tag + name + " who is alive has birthdate less than 150 years from now")


def US36():
    query = "SELECT NAME,ALIVE,DEATH FROM INDIVIDUAL"

    result = conn.execute(query)
    rows = result.fetchall()

    date_format = "%d %b %Y"
    today = datetime.today().date()

    recent_deaths = []

    for row in rows:
        if row[1] == "False":  # If the person is dead..

            death_date = datetime.strptime(row[2], date_format).date()
            difference = today - death_date

            if difference.days <= 30:
                recent_deaths.append(row[0].replace("/", ""))  # print Name

    if len(recent_deaths) > 0:
        for person in recent_deaths:
            print("ERROR: US36: " + person + " died in the last 30 days")

    def deadRecently(name):

        if name in recent_deaths:
            return True

        return False

def US01():
    current = datetime.now().date()
    query1 = "select NAME,BIRTHDAY,DEATH from INDIVIDUAL"
    result1 = conn.execute(query1)
    value1 = result1.fetchall()
    i = 0
    date_format = "%d %b %Y"
    for row in value1:
        first_row = value1[i]

        a = datetime.strptime(first_row[1], '%d %b %Y').date()
        if (first_row[2] == 'NA'):
            pass
        else:
            c = datetime.strptime(first_row[2], '%d %b %Y').date()
            # c.strftime('%d %m %Y')
                # print c
        if (c == 'NA'):
            pass
        elif (c != 'NA' and (current < a or current < c)):

            print('ERROR: US01: ' + first_row[1].replace("/", " ") + ' is after the current date ')

        i += 1

    query2 = "select HUSBAND_NAME,WIFE_NAME,MARRIED,DIVORCED from FAMILY"
    result2 = conn.execute(query2)
    value2 = result2.fetchall()
    j = 0
    e = 'NA'
    for row in value2:
        first_row = value2[j]
        #d=datetime.strptime(first_row[2],'%d %b %Y').date()
            # print a
        if (first_row[3] == 'NA'):
            pass
        else:
            e = datetime.datetime.strptime(first_row[3], '%d %b %Y').date()

        if (e == 'NA'):
            pass
        elif (current < e):
            print("ERROR: US01: ", first_row[2].replace("/", " "), " is after the current date ")

        j += 1

def US12():
    query = "SELECT I1.BIRTHDAY AS HUSBAND_BIRTHDAY, I2.BIRTHDAY AS WIFE_BIRTHDAY, I3.BIRTHDAY as CHILD_BIRTHDAY,F1.HUSBAND_NAME,F2.WIFE_NAME FROM INDIVIDUAL I1 INNER JOIN INDIVIDUAL I2 ON I1.ID <> I2.ID INNER JOIN INDIVIDUAL I3 ON I1.ID<>I3.ID AND I2.ID<> I3.ID INNER JOIN FAMILY F1 ON F1.HUSBAND_ID = I1.ID INNER JOIN FAMILY F2 ON F2.WIFE_ID=I2.ID INNER JOIN FAMILY F3 ON I3.CHILD=F3.ID WHERE F1.ID=F2.ID AND F3.ID=F1.ID"
    result1 = conn.execute(query)
    value1 = result1.fetchall()
    i = 0
    date_format = "%d %b %Y"
    for row in value1:
        first_row = value1[i]
        husband_birthday = datetime.strptime(first_row[0], date_format).date()

        wife_birthday = datetime.strptime(first_row[1], date_format).date()

        child_birthday = datetime.strptime(first_row[2], date_format).date()

        husband_child_diff = husband_birthday - child_birthday

        husband_child_yearsdiff = husband_child_diff.days / 365

        wife_child_diff = husband_birthday - child_birthday

        wife_child_yearsdiff = wife_child_diff.days / 365
        if ((husband_child_yearsdiff > 80) and (wife_child_yearsdiff > 60)):
            print("ERROR: US12: " + first_row[3].replace("/", " ") + " or " + first_row[4].replace("/",
                                                                                                       " ") + " have a child either more than 60 years younger than mother or more than 80 years younger than father")

        i += 1

def US14():
    query = "SELECT ID,CHILDREN from FAMILY"

    result = conn.execute(query)
    data = result.fetchall()

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ","]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData
    def US14mulsib():

        for familyData in data:
            famId = familyData[0]
            children = familyData[1]

            siblings = formatChildrenData(children)

            noOfSiblings = len(siblings)
            #print(noOfSiblings)
            if (noOfSiblings >= 5):
                #print(".")
                famObj = Family.Family()
                famObj.setFamId(famId)

                for indi_id in siblings:
                    birth_date_query = conn.execute("SELECT BIRTHDAY from INDIVIDUAL where ID = ?", (indi_id,))
                    birthdates = birth_date_query.fetchall()
                    for dates in birthdates:
                        #print(dates[0])
                        myBirthDate = datetime.strptime(dates[0], '%d %b %Y').date()
                        famObj.setBirthdate(myBirthDate)

                val,checkSiblings = famObj.validateNoOfSiblings()
                #print(checkSiblings)
                if (checkSiblings):
                    print("ERROR: US14: ", famObj.getFamId() + " has " + str(noOfSiblings) + " siblings " + "from which "+ str(val)+ " have same birth day")
    US14mulsib()

# User stories by Shreyas
US22()
US13()
US14()
US19()

# User stories by Pranit
US16()
US21()
US07()
US36()

# User stories by Aakanksha
US25()
US29()
US10()
US11()

# User stories by Rishi
US03()
US02()
US01()
US12()


conn.close()
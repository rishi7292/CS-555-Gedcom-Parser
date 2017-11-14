import sqlite3
from _datetime import datetime
import re
import Family
import pandas as pd
import GEDCOM_parser
import operator
import datetime as DT

conn = sqlite3.connect('DATA_Sprint4.db')
conn.text_factory = str

indi_table = pd.read_sql_query('SELECT * FROM INDIVIDUAL', conn)
fam_table = pd.read_sql_query('SELECT * FROM FAMILY', conn)
print('INDIVIDUAL TABLE')
print(indi_table)
print('FAMILY TABLE')
print(fam_table)

def getRecentDead():
    query = "SELECT NAME,ALIVE,DEATH,ID FROM INDIVIDUAL"
    ID = []
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
                ID.append(row[3])

    return recent_deaths,ID

#Shreyas Sule
def US34():
    Result_query = "select Husband_name,wife_name,married,I1.birthday as husband_birthday,I2.birthday as wife_birthday from FAMILY as F,INDIVIDUAL as I1,INDIVIDUAL as I2 where I1.ID=F.husband_id and I2.ID=F.wife_id"
    Final_result = conn.execute(Result_query)
    Final_value = Final_result.fetchall()

    for Each_row in Final_value:
        if (Each_row[2] == 'NA' or Each_row[3] == 'NA' or Each_row[3] == 'NA'):
            pass
        else:
            Marriage_date = datetime.strptime(Each_row[2], '%d %b %Y').date()
            Husband_birthdate = datetime.strptime(Each_row[3], '%d %b %Y').date()
            Wife_birthdate = datetime.strptime(Each_row[4], '%d %b %Y').date()

            husband_age = Marriage_date - Husband_birthdate
            wife_age = Marriage_date - Wife_birthdate

            if (husband_age > 2 * wife_age or wife_age > 2 * husband_age):
                print("ERROR: US34:", Each_row[0].replace("/", ""), " or ", Each_row[1].replace("/", ""),
                      " have a greater age difference")


# Pranit Kulkarni
def US08():
    query = "SELECT MARRIED,DIVORCED,CHILDREN FROM FAMILY"

    date_format = "%d %b %Y"

    error_tag = "ERROR: US08: "

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ","]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData

    def getChildBirthDate(child_id):
        result = conn.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID = ?", (child_id,))
        cursor = result.fetchone()

        if cursor == None:
            return None

        birthdate_text = cursor[0]

        if (birthdate_text != "NA"):
            birthdate = datetime.strptime(birthdate_text, date_format).date()

            return birthdate

        return None

    invalid_births = []

    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:
        married_date_text = row[0]
        divorce_date_text = row[1]

        parents_marriage_date = None

        if married_date_text != 'NA':
            parents_marriage_date = datetime.strptime(married_date_text, date_format).date()

        parents_divorce_date = None

        if divorce_date_text != 'NA':
            parents_divorce_date = datetime.strptime(divorce_date_text, date_format).date()

        children = formatChildrenData(row[2])

        if len(children) > 0:

            for child in children:
                child_birth_date = getChildBirthDate(child)

                if child_birth_date != None and parents_marriage_date != None:

                    if child_birth_date < parents_marriage_date:
                        invalid_births.append(child)
                        print(error_tag + " " + child + " has birthdate before parent's marriage date")
                    elif parents_divorce_date != None:
                        if child_birth_date > parents_divorce_date:
                            difference = child_birth_date - parents_divorce_date

                            months = difference.days / 30

                            if months > 9:
                                invalid_births.append(child)
                                print(error_tag + " " + child + " has birthdate 9 months after parent's divorce date")

    if len(invalid_births) == 0:
        print("No invalid births found")


def US35():
    query = "SELECT NAME,BIRTHDAY FROM INDIVIDUAL"

    date_format = "%d %b %Y"
    today = datetime.today().date()

    recent_births = []

    result = conn.execute(query)
    rows = result.fetchall()

    for row in rows:

        birth_date = datetime.strptime(row[1], date_format).date()
        difference = today - birth_date

        if difference.days <= 30:
            recent_births.append(row[0].replace("/", ""))  # print Name

    if len(recent_births) > 0:
        print("US 35: List of people who were born in the last 30 days")

        for person in recent_births:
            print(person)
    else:
        print("US 35: No birth in last 30 days")




#Rishi Manjrekar -- Sprint 4
def US39():
    flag = 0
    current_date = datetime.now().date()
    # print "Current Date is: ",current_date
    current_day = current_date.day
    current_month = current_date.month

    end_date = current_date + DT.timedelta(days=30)
    # print "After 30 days the date is: ",end_date

    Result_query = "select distinct F.Husband_name,F.wife_name,F.married from FAMILY as F,INDIVIDUAL as I where (F.husband_id=I.Id or F.wife_id=I.id) and I.death='NA' and F.married!='NA'"
    Final_result = conn.execute(Result_query)
    Final_value = Final_result.fetchall()

    for Each_row in Final_value:
        if (Each_row[2] == 'NA'):
            pass
        else:
            converted_date = datetime.strptime(Each_row[2], '%d %b %Y').date()
            converted_day = converted_date.day
            converted_month = converted_date.month

            if (converted_month - current_month == 0 and converted_day - current_day > 0):
                flag = 1
                print("US39: ", Each_row[0].replace("/", " "), "and", Each_row[1].replace("/"," "), "have a upcoming marriage anniversary")
            elif (converted_month - current_month == 1 and (converted_day - current_day > 0 or current_day - converted_day > 0)):
                flag = 1
                print("US39: ", Each_row[0].replace("/", " "), "and", Each_row[1].replace("/"," "), "have a upcoming marriage anniversary")
    if(flag == 0):
        print("US39: No upcoming marriage anniversary")


def US04():
    Result_query = "select husband_name,wife_name,married,divorced from FAMILY"
    Final_result = conn.execute(Result_query)
    Final_value = Final_result.fetchall()

    for Each_row in Final_value:
        if (Each_row[2] == 'NA' or Each_row[3] == 'NA'):
            pass
        else:
            Marriage_date = datetime.strptime(Each_row[2], '%d %b %Y').date()
            Divorce_date = datetime.strptime(Each_row[3], '%d %b %Y').date()

            if (Divorce_date < Marriage_date):
                print("ERROR: US04:", Each_row[0].replace("/", " "), "and", Each_row[1].replace("/"," "), "have a Divorce date before their Marriage date")

#Aakanksha Gokhe -- Sprint 4
def US38():
    ID = []
    name = []
    birthday = []
    check_list = []
    flag = 0
    cur = conn.cursor()
    cur.execute("SELECT ID,NAME,BIRTHDAY FROM INDIVIDUAL WHERE ALIVE='True'")
    rows = cur.fetchall()
    for id, nm, bd in rows:
        ID.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(id)))
        name.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(nm)))
        birthday.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(bd)))
    for p, bd in enumerate(birthday):
        d1 = datetime.strptime(bd, "%d %b %Y")
        start_date = datetime.now()
        end_date = datetime.now() + DT.timedelta(30)
        if ((start_date.month, start_date.day) <= (d1.month, d1.day) and (end_date.month, end_date.day) >= (
        d1.month, d1.day)):
            flag = 1
            check_list.append(name[p])
            print("US38: UPCOMING BIRTHDAY OF", ID[p], "-", name[p], ": Birth Date-", bd)
    if (flag == 0):
        print("US38: NO UPCOMING BIRTHDAYS! :((")
def US15():
    Fam_ID = []
    siblings = []
    err = []
    cur = conn.cursor()
    cur.execute("SELECT ID,CHILDREN FROM FAMILY")
    rows = cur.fetchall()
    for id,chld in rows:
        Fam_ID.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(id)))
        siblings.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(chld)))
    for p,sib in enumerate(siblings):
        sib_List = sib.split(',')
        if(len(sib_List)>=15):
            err.append(Fam_ID[p])
            print("ERROR: US15: Family-",Fam_ID[p]," has more than 15 siblings in the family")

#Pranit Kulkarni
def US18():
    query = "SELECT HUSBAND_ID,WIFE_ID FROM FAMILY"

    def getFamilyId(id):
        query = "SELECT ID FROM FAMILY WHERE CHILDREN LIKE '%" + id + "%' "
        result = conn.execute(query)
        cursor = result.fetchone()
        if (cursor == None):
            return None
        # print("Family ID found: "+cursor[0]+" for "+id)
        return cursor[0]

    def US18_main():
        result = conn.execute(query)
        rows = result.fetchall()

        for row in rows:
            husband_id = row[0]
            wife_id = row[1]

            husband_family_id = getFamilyId(husband_id)
            wife_family_id = getFamilyId(wife_id)

            if (husband_family_id == wife_family_id and husband_family_id != None):
                print("ERROR: US18: " + husband_id + " and " + wife_id + " who are married are siblings")

    US18_main()


def US09():
    query = "SELECT HUSBAND_ID,WIFE_ID FROM FAMILY"

    date_format = "%d %b %Y"

    def getDeathDate(id):
        # print(id)
        query = "SELECT DEATH FROM INDIVIDUAL WHERE ALIVE = 'False' AND ID = ?", (id,)
        result = conn.execute("SELECT DEATH FROM INDIVIDUAL WHERE ALIVE = 'False' AND ID = ?", (id,))
        row = result.fetchone()

        if row == None:
            return None

        return row[0]

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ","]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData

    def getChildBirthDate(id):
        # query = "SELECT BIRTH FROM INDIVIDUAL WHERE ID = "+id
        cursor = conn.execute("SELECT BIRTHDAY FROM INDIVIDUAL WHERE ID = ?", (id,))
        result = cursor.fetchone()

        if result == None:
            return None

        birthdate = result[0]

        return birthdate

    def calculateDifference(child_birth_date, father_death_date, mother_death_date):
        if child_birth_date != None:
            birthdate = datetime.strptime(child_birth_date, date_format).date()

            if mother_death_date != None:
                deathdate = datetime.strptime(mother_death_date, date_format).date()

                if birthdate > deathdate:
                    print("ERROR: US09: ")

    def US09_main():
        result = conn.execute(query)
        rows = result.fetchall()

        for row in rows:
            father_id = row[0]
            mother_id = row[1]

            father_death_date = getDeathDate(father_id)
            mother_death_date = getDeathDate(mother_id)

            # query = "SELECT CHILDREN FROM FAMILY WHERE HUSBAND_ID = "+father_id
            result = conn.execute("SELECT CHILDREN FROM FAMILY WHERE HUSBAND_ID = ?", (father_id,))
            cursor = result.fetchone()
            children = cursor[0]

            childrenList = formatChildrenData(children)

            if len(childrenList) > 0:
                for child in childrenList:
                    child_birth_date = getChildBirthDate(child)

                    if child_birth_date != None:
                        birthdate = datetime.strptime(child_birth_date, date_format).date()

                        if mother_death_date != None:
                            deathdate = datetime.strptime(mother_death_date, date_format).date()

                            if birthdate > deathdate:
                                print("ERROR: US09: " + child + " is born after the death of his mother " + mother_id)

                        if father_death_date != None:
                            deathdate = datetime.strptime(father_death_date, date_format).date()
                            # difference = monthdelta(birthdate,deathdate)    # Gets difference in months..
                            difference = deathdate - birthdate
                            months = difference.days / 30

                            if deathdate < birthdate and months > 9:
                                print(
                                    "ERROR: US09: " + child + " is born 9 months after the death of his father " + father_id)

    US09_main()


#Aakanksha Gokhe
def US28():
    FAM_ID = []
    Children_ID = []
    #conn = sqlite3.connect('DATA.db')
    cur = conn.cursor()
    cur.execute("SELECT ID,CHILDREN FROM FAMILY")
    rows = cur.fetchall()
    print("US28-")
    for fid, chld in rows:
        FAM_ID.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(fid)))
        Children_ID.append(re.sub(r'[^@,0-9a-zA-Z ]+', '', str(chld)))
    for pos, id in enumerate(FAM_ID):
        sib_dict = {}
        # name = []
        sib_list = Children_ID[pos].split(',')
        # print(sib_list)
        if (len(sib_list) > 1):
            for sid in sib_list:
                cur.execute("SELECT NAME,AGE FROM INDIVIDUAL WHERE ID=?", (sid,))
                rows1 = cur.fetchall()
                # name.append(re.sub(r'[^A-Za-z ]+','',str(rows1[0][0])))
                age = int(re.sub(r'[^0-9]', '', str(rows1[0][1])))
                sib_dict[sid] = age
            # print(name)
            sorted_sib_dict = sorted(sib_dict.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_sib_dict)
            print("FOR FAMILY ID - ", id)
            for pos, info in enumerate(sorted_sib_dict):
                cur.execute("SELECT NAME FROM INDIVIDUAL WHERE ID=?", (info[0],))
                rn = cur.fetchall()
                name = re.sub(r'[^A-Za-z ]+', '', str(rn[0]))
                print(name, info[1])

def US06():
    HID = []
    WID = []
    Div_date = []

    def compare_dates(husb_death, wife_death, divorce):

        if (husb_death == 'NA'):
            if(wife_death == 'NA'):
                pass
            else:
                wife_death = datetime.strptime(str(wife_death), "%d %b %Y")
                wife_death = datetime.date(wife_death)
                divorce = datetime.strptime(str(divorce), "%d %b %Y")
                divorce = datetime.date(divorce)
                if (divorce > wife_death):
                    return True
                else:
                    return False
        elif (wife_death == 'NA'):
            if(husb_death == 'NA'):
                pass
            else:
                husb_death = datetime.strptime(str(husb_death), "%d %b %Y")
                husb_death = datetime.date(husb_death)
                divorce = datetime.strptime(str(divorce), "%d %b %Y")
                divorce = datetime.date(divorce)
                if (divorce > husb_death):
                    return True
                else:
                    return False
        else:
            husb_death = datetime.strptime(str(husb_death), "%d %b %Y")
            husb_death = datetime.date(husb_death)
            wife_death = datetime.strptime(str(wife_death), "%d %b %Y")
            wife_death = datetime.date(wife_death)
            divorce = datetime.strptime(str(divorce), "%d %b %Y")
            divorce = datetime.date(divorce)
            if (divorce > husb_death or divorce > wife_death):
                return True
            else:
                return False

    cur = conn.cursor()
    cur.execute("SELECT HUSBAND_ID,WIFE_ID,DIVORCED FROM FAMILY")
    rows = cur.fetchall()
    for hid, wid, divdt in rows:
        HID.append(re.sub(r'[^@0-9a-zA-Z ]+', '', str(hid)))
        WID.append(re.sub(r'[^@0-9A-Za-z]+', '', str(wid)))
        Div_date.append(re.sub(r'[^0-9a-zA-Z ]+', '', str(divdt)))

    for pos, id in enumerate(HID):
        cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?", (id,))
        info = cur.fetchall()
        cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?", (WID[pos],))
        info1 = cur.fetchall()
        death_date_husb = re.sub(r'[^0-9a-zA-Z ]', '', str(info[0]))
        death_date_wife = re.sub(r'[^0-9a-zA-Z ]', '', str(info1[0]))
        if (Div_date[pos] != 'NA'):
            result = compare_dates(death_date_husb, death_date_wife, Div_date[pos])
            if (result):
                print("ERROR: US06: ", id, " and ", WID[pos], " are divorced after the death of either spouse")

#Shreyas Sule
def US20():
    result = conn.execute("SELECT ID,CHILDREN from FAMILY")
    data = result.fetchall()

    alreadySearched = []

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ",", "(", ")"]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData

    def us20():

        for family in data:
            famId = family[0]
            children = family[1]

            siblings = formatChildrenData(children)
            if (len(siblings) >= 1):
                for indi_id in siblings:
                    flag = 0
                    # Get Parents of the current child
                    parent_query = conn.execute(
                        "SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT CHILD from INDIVIDUAL where ID = ?)",
                        (indi_id,))
                    myParents = parent_query.fetchone()

                    my_parents_siblings = []  # this list will contain all the aunts and uncles of the current child
                    if (myParents != None):
                        father = myParents[0]
                        mother = myParents[1]

                        # get the id of family where my father is the child
                        father_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?", (father,))
                        father_family = father_family_query.fetchall()
                        father_family = [i[0] for i in father_family]

                        if (father_family[0] != 'NA'):
                            for fatherId in father_family:

                                # Get siblings of my father i.e my aunts and uncles from father's side
                                siblingsOfFatherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",
                                                                     (fatherId,))
                                siblingsOfFather = siblingsOfFatherQuery.fetchall()
                                siblingsOfFather = [i[0] for i in siblingsOfFather]
                                siblingsOfFather = re.sub(r'[^@I0-9,]', '', siblingsOfFather[0])
                                siblingsOfFather = siblingsOfFather.split(",")

                                # Store all siblings of father except father himself.
                                for fathersiblingId in siblingsOfFather:
                                    if (fathersiblingId != fatherId):
                                        my_parents_siblings.append(fathersiblingId)

                        # Get siblings of my mother i.e my aunts and uncles from mother's side.
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

                                # Store all siblings of mother except mother herself.
                                for mothersiblingId in siblingsOfMother:
                                    if (mothersiblingId != motherId):
                                        my_parents_siblings.append(mothersiblingId)
                    # print("list "+str(my_parents_siblings))
                    for my_parents_siblingsId in my_parents_siblings:
                        my_parents_siblings_spouseQuery = conn.execute(
                            "SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL where ID = ?)",
                            (my_parents_siblingsId,))
                        my_parents_siblings_spouse = my_parents_siblings_spouseQuery.fetchone()

                        if (my_parents_siblings_spouse != None):
                            my_parents_siblings_spouse = list(my_parents_siblings_spouse)
                            # print(my_parents_siblings_spouse)
                            husband = my_parents_siblings_spouse[0]
                            wife = my_parents_siblings_spouse[1]

                            partner = ""
                            if (husband != my_parents_siblingsId):
                                partner = husband

                            else:
                                partner = wife
                            # print(partner)
                            if partner in my_parents_siblings:
                                if partner in alreadySearched and my_parents_siblingsId in alreadySearched:
                                    flag = 1
                                    return flag, 1
                                else:
                                    flag = 0
                                    alreadySearched.append(partner)
                                    alreadySearched.append(my_parents_siblingsId)
                                    return alreadySearched, flag, 0

    chk, f, x = us20()
    if (f == 0 and x == 0):
        invalidIds = ",".join(chk)
        #for id in chk:
        #    invalidIds += "," + id
        print("Error : US20 IDs-" + invalidIds + " are aunts and uncles and should not be married")


def US30():
    livingMarried = []
    result = conn.execute("SELECT ID,ALIVE,SPOUSE from INDIVIDUAL")
    data = result.fetchall()

    for indi in data:
        indi_id = indi[0]
        alive = indi[1]
        spouse = indi[2]

        # print(indi_id+" "+alive+" "+spouse)

        if (spouse != 'NA' and alive == 'True'):
            livingMarried.append(indi_id)

    str = ""
    for id in livingMarried:
        str += id + " "

    print("US30 : List of living married is : " + str)


#Rishi

def US31():
    Result_query = "select ID,name,age from INDIVIDUAL where spouse='NA' and age>30 and death='NA'"
    Final_result = conn.execute(Result_query)
    Final_value = Final_result.fetchall()
    for Each_row in Final_value:
        print("ERROR: US31: " + Each_row[1].replace("/", " ") + "is single and alive and has a age of", Each_row[2], " which is more than 30")


def US23():
    query = "select distinct I1.name,I1.birthday from INDIVIDUAL as I1,INDIVIDUAL as I2 where I1.ID!=I2.ID and I1.name=I2.name and I1.birthday=I2.birthday"
    result = conn.execute(query)
    value = result.fetchall()

    for each_row in value:
        print("ERROR: US23:", each_row[0].replace("/", " "), "has birthday on", each_row[1], " and appears more than one time")



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
            # print(error_tag + "The family id " + id + " has no child")
            pass
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
    # query = "SELECT NAME,ALIVE,DEATH FROM INDIVIDUAL"
    #
    # result = conn.execute(query)
    # rows = result.fetchall()
    #
    # date_format = "%d %b %Y"
    # today = datetime.today().date()
    #
    # recent_deaths = []
    #
    # for row in rows:
    #     if row[1] == "False":  # If the person is dead..
    #
    #         death_date = datetime.strptime(row[2], date_format).date()
    #         difference = today - death_date
    #
    #         if difference.days <= 30:
    #             recent_deaths.append(row[0].replace("/", ""))  # print Name
    recent_deaths,ID = getRecentDead()
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
            e = datetime.strptime(first_row[3], '%d %b %Y').date()

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

#Shreyas
def US37():
    recent_deaths,ID = getRecentDead()

    def formatChildrenData(siblings):
        punctuation = ["{", "}", ",", "(", ")"]
        for characters in punctuation:
            siblings = siblings.replace(characters, " ").strip()
        childrenData = siblings.split(" ")
        return childrenData

    def recent_survivors():

        for id in ID:

            # if the id has no spouse
            validation_query = conn.execute("SELECT SPOUSE FROM INDIVIDUAL WHERE ID = ?", (id,))
            validation_query_result = validation_query.fetchone()
            if (validation_query_result == 'NA'):
                print(id + " was single")
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
                        child_str += child_id + " "
                    if (id == husband_id):
                        print("ERROR: US37: ",id + " died in last 30 days and was the husband of  " + wife_id + " and had " + child_str + " as their children who survived")
                    elif (id == wife_id):
                        print("ERROR: US37: ",id + " died in last 30 days and was the wife of " + husband_id + " and had " + child_str + " as their children who survived")

    recent_survivors()

# User stories by Shreyas
US22()
US13()
US14()
US19()
US30()
US20()
US34()
US37()

# User stories by Pranit
US16()
US21()
US07()
US36()
US09()
US18()
US08()
US35()

# User stories by Aakanksha
US25()
US29()
US10()
US11()
US06()
US28()
US15()
US38()

# User stories by Rishi
US03()
US02()
US01()
US12()
US23()
US31()
US04()
US39()

conn.close()
import sqlite3
import re

conn = sqlite3.connect("GEDCOM_DATA_US20.db")
conn.text_factory = str

result = conn.execute("SELECT ID,CHILDREN from FAMILY")
data = result.fetchall()

alreadySearched = []
def formatChildrenData(siblings):
    punctuation = ["{","}",",","(",")"]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData

def us20():

    for family in data:
        famId = family[0]
        children = family[1]

        siblings = formatChildrenData(children)
        if(len(siblings) >= 1):
            for indi_id in siblings:
                flag = 0
                #Get Parents of the current child
                parent_query = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT CHILD from INDIVIDUAL where ID = ?)",(indi_id,))
                myParents = parent_query.fetchone()

                my_parents_siblings = [] #this list will contain all the aunts and uncles of the current child
                if(myParents != None):
                    father = myParents[0]
                    mother = myParents[1]

                    #get the id of family where my father is the child
                    father_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(father,))
                    father_family = father_family_query.fetchall()
                    father_family = [i[0] for i in father_family]

                    if(father_family[0] != 'NA'):
                        for fatherId in father_family:

                            #Get siblings of my father i.e my aunts and uncles from father's side
                            siblingsOfFatherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(fatherId,))
                            siblingsOfFather = siblingsOfFatherQuery.fetchall()
                            siblingsOfFather = [i[0] for i in siblingsOfFather]
                            siblingsOfFather = re.sub(r'[^@I0-9,]','',siblingsOfFather[0])
                            siblingsOfFather = siblingsOfFather.split(",")

                            #Store all siblings of father except father himself.
                            for fathersiblingId in siblingsOfFather:
                                if(fathersiblingId != fatherId):
                                    my_parents_siblings.append(fathersiblingId)

                    #Get siblings of my mother i.e my aunts and uncles from mother's side.
                    mother_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(mother,))
                    mother_family = mother_family_query.fetchall()
                    mother_family = [i[0] for i in mother_family]

                    if(mother_family[0] != 'NA'):

                        for motherId in mother_family:
                            siblingsOfMotherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(motherId,))
                            siblingsOfMother = siblingsOfMotherQuery.fetchall()
                            siblingsOfMother = [i[0] for i in siblingsOfMother]
                            siblingsOfMother = re.sub(r'[^@I0-9,]','',siblingsOfMother[0])
                            siblingsOfMother = siblingsOfMother.split(",")

                            #print(siblingsOfMother)

                                #Store all siblings of mother except mother herself.
                            for mothersiblingId in siblingsOfMother:
                                if(mothersiblingId != motherId):
                                    my_parents_siblings.append(mothersiblingId)
                #print("list "+str(my_parents_siblings))
                for my_parents_siblingsId in my_parents_siblings:
                    my_parents_siblings_spouseQuery = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL where ID = ?)",(my_parents_siblingsId,))
                    my_parents_siblings_spouse = my_parents_siblings_spouseQuery.fetchone()
                    
                    
                    if(my_parents_siblings_spouse != None):
                        my_parents_siblings_spouse = list(my_parents_siblings_spouse)
                        #print(my_parents_siblings_spouse)
                        husband = my_parents_siblings_spouse[0]
                        wife = my_parents_siblings_spouse[1]

                        partner = ""
                        if(husband != my_parents_siblingsId):
                            partner = husband
                            
                        else:
                            partner = wife
                        #print(partner)
                        if partner in my_parents_siblings:
                            if partner in alreadySearched and my_parents_siblingsId in alreadySearched:
                                flag = 1
                                return flag,1
                            else:
                                flag = 0
                                alreadySearched.append(partner)
                                alreadySearched.append(my_parents_siblingsId)
                                return alreadySearched,flag,0

chk,f,x = us20()
if(f == 0 and x == 0):
    invalidIds = ""
    for id in chk:
        invalidIds += " "+id
    print("Error : US20 IDs "+invalidIds+" are aunts and uncles and should not be married")


                            
    
                



import sqlite3
#import Cousins
import re
conn = sqlite3.connect("GEDCOM_DATA_US19.db")
conn.text_factory = str

result = conn.execute("SELECT ID,CHILDREN from FAMILY")
data = result.fetchall()
chk = []
def formatChildrenData(siblings):
    punctuation = ["{","}",",","(",")"]
    for characters in punctuation:
        siblings = siblings.replace(characters," ").strip()
    childrenData = siblings.split(" ")
    return childrenData

def us19FirstCousins():
    
    for familyData in data:
        famId = familyData[0]
        children = familyData[1]

        siblings = formatChildrenData(children)
        #print(siblings)
        if(len(siblings) >= 1):
            for indi_id in siblings:
                flag = 0
                #Get parents of current child
                parent_query = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT CHILD from INDIVIDUAL where ID = ?)",(indi_id,))
                parents = parent_query.fetchone()
                #print(parents)
                #parents = list(parents)
                #print(parents)
                cousins = []
                parents_siblings = []
                if(parents != None):
                    father = parents[0]
                    #print(father)   
                    mother = parents[1]

                        
                    father_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(father,))
                    father_family = father_family_query.fetchall()
                    father_family = [i[0] for i in father_family]
                    #print(father_family)

                    if(father_family[0] != 'NA'):

                        for fatherId in father_family:
                            siblingsOfFatherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(fatherId,))
                            siblingsOfFather = siblingsOfFatherQuery.fetchall()
                            siblingsOfFather = [i[0] for i in siblingsOfFather]
                            siblingsOfFather = re.sub(r'[^@I0-9,]','',siblingsOfFather[0])
                            siblingsOfFather = siblingsOfFather.split(",")
                            #print(siblingsOfFather)
                                #Store all siblings of father except father himself.
                            for siblingId in siblingsOfFather:
                                if(siblingId != fatherId):
                                    parents_siblings.append(siblingId)
                    #print(parents_siblings)


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

                                #Store all siblings of father except father himself.
                            for siblingId in siblingsOfMother:
                                if(siblingId != motherId):
                                    parents_siblings.append(siblingId)
                    
                        #print(parent_siblings+" all siblings ")

                    #print(parents_siblings)
                        
                    for parentSiblingIds in parents_siblings:
                        
                        """
                        parentSiblingIds = list(parentSiblingIds)
                        parentSiblingIds = re.sub(r'[^@I0-9,]','',parentSiblingIds[0])
                        parentSiblingIds = parentSiblingIds.split(',')
                        """
                            #print(parentSiblingIds)

                        
                        cousinFamilyQuery = conn.execute("SELECT SPOUSE from INDIVIDUAL where ID = ?",(parentSiblingIds,))

                        cousinFamilyId = cousinFamilyQuery.fetchall()
                        cousinFamilyId = [i[0] for i in cousinFamilyId]
                        #print(cousinFamilyId)
                                
                        for cId in cousinFamilyId:
                            
                            if(cousinFamilyId != None):
                                    
                                cousinsQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(cId,))
                                cousinData = cousinsQuery.fetchone()
                                if(cousinData!=None):

                                    cousinData = list(cousinData)
                                    cousinData = re.sub(r'[^@I0-9,]','',cousinData[0])
                                    cousinData = cousinData.split(',')
                                    for i in cousinData:
                                        cousins.append(i)
                                    #print(cousins)
                                
                                    for id in cousins:
                                        mySpouseQuery = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL where ID = ?)",(id,))
                                        mySpouse = mySpouseQuery.fetchone()
                                        if(mySpouse!=None):
                                            mySpouse = list(mySpouse)
                                            husband = mySpouse[0]
                                            wife = mySpouse[1]
                                            #print(husband,wife)
                                    if husband in cousins and wife in cousins:
                                        if husband in chk and wife in chk:
                                            flag = 1
                                            return flag, 1
                                            #h = husband
                                            #w = wife
                                            #flag = 1
                                        else:
                                            flag = 0
                                            chk.append(husband)
                                            chk.append(wife)
                                            return chk,flag,0
        #if(flag == 1):
            #flag1 = 1
            #print("ERROR: US19: ID-",h," and ",w,"are first cousins and married")
chk1,f,x = us19FirstCousins()
if(f==0 and x==0):
    ids1 = ",".join(chk1)
    print("ERROR: US19: IDs",ids1," are first cousins and married")
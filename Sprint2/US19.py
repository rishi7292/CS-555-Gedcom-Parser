import sqlite3
import Cousins
import re
conn = sqlite3.connect("GEDCOM_DATA_US19.db")
conn.text_factory = str

result = conn.execute("SELECT ID,CHILDREN from FAMILY")
data = result.fetchall()

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

        if(len(siblings) >= 1):
            for indi_id in siblings:
                
                #Get parents of current child
                parent_query = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT CHILD from INDIVIDUAL where ID = ?)",(indi_id,))
                parents = parent_query.fetchone()
                #print(parents)
                #parents = list(parents)
                #print(parents)
                
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
                                    #print(cousinData)
                                        
                                #cousins = formatChildrenData(cousinData[0])
                            #print(cousins)
                                
                                    for id in cousinData:
                                        mySpouseQuery = conn.execute("SELECT HUSBAND_ID,WIFE_ID from FAMILY where ID in (SELECT SPOUSE from INDIVIDUAL where ID = ?)",(id,))
                                        mySpouse = mySpouseQuery.fetchone()
                                        if(mySpouse!=None):
                                            mySpouse = list(mySpouse)
                                            #print(mySpouse)
                                            #if(mySpouse != None):
                                                
                                            for spId in mySpouse:

                                                if spId in cousinData and id!=spId:
                                                    print("ERROR")
                                                        #continue
                            """
                            for spouse_id in cousins:
                                    #print(spouse_id)
                                if(mySpouse[0] == spouse_id):
                                    print("LAFDEBAZ FAMILY")
                            """
                        
                
                """
                #Get family of parent's parent
                for ids in parents:
                    father = parents[0]
                    mother = parents[1]

                    
                    father_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(father))
                    father_family = father_family_query.fetchall()

                    #get all siblings for father's family
                    for fatherId in father_family:
                        siblingsOfFatherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(fatherId))
                        siblingsOfFather = siblingsOfFatherQuery.fetchall()

                        #Store all siblings of father except father himself.
                        for siblingId in siblingsOfFather:
                            if(siblingId[0] != fatherId):
                                parent_siblings.append(siblingId)



                    mother_family_query = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(mother))
                    mother_family = mother_family_query.fetchall()
                    for motherId in mother_family:
                        siblingsOfMotherQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(motherId))
                        siblingsOfMother = siblingsOfMotherQuery.fetchall()

                        #Store all siblings of father except father himself.
                        for siblingId in siblingsOfMother:
                            if(siblingId[0] != motherId):
                                parent_siblings.append(siblingId)
                    
                    for parentSiblingIds in parent_siblings:
                        cousinFamilyQuery = conn.execute("SELECT CHILD from INDIVIDUAL where ID = ?",(parentSiblingIds))
                        cousinFamilyId = cousinsQuery.fetchone()[0]
                        cousinsQuery = conn.execute("SELECT CHILDREN from FAMILY where ID = ?",(cousinFamilyId))
                        cousinData = cousinsQuery.fetchone()[0]

                        cousins = formatChildrenData(cousins)

                        mySpouseQuery = conn.execute("SELECT SPOUSE from INDIVIDUAL where ID = ?",(indi_id))
                        mySpouse = mySpouseQuery.fetchone()[0]

                        for spouse_id in cousins:
                            if(mySpouse == spouse_id):
                                print("LAFDEBAZ FAMILY")
                """


us19FirstCousins()
                        


                            
                    





                
                    








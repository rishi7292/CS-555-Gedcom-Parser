import sqlite3

conn = sqlite3.connect("GEDCOM_DATA.db")
conn.text_factory = str

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

for row in INDI_ID:
    print row

for ID in all_FAM_IDs:
    FAM_ID.append(ID[0])


def isINDIUnique():
    if(len(INDI_ID) == len(set(INDI_ID))):
        return True
    return False

def isFamUnique():
    if(len(FAM_ID) == len(set(FAM_ID))):
        return True
    return False

def getIdFromINDI(Indi_ID):
    if Indi_ID in INDI_ID:
        return Indi_ID
    return

def getIdFromFAM(Fam_id):
    if Fam_id in FAM_ID:
        return Fam_id
    


    

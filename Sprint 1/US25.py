import sqlite3
import re
flag = 0
c = []
fam_id = []
children_id = []
name = []
bday = []
conn = sqlite3.connect('GEDCOM_DATA.db')
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
        print("The family id -", id, " has no child")
    else:
        if len(name) != len(set(name)) and len(bday) != len(set(bday)):
            print("The children of family id -", id, " does not have unique first names!")
        else:
            print("The children of family id -", id, " has unique first names!")
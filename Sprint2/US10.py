import sqlite3
import re
from datetime import datetime
def age_at_marriage(d1,d2):
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
conn = sqlite3.connect('DATA.db')
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
    if age < 14 and age>0:
        under_age.append(hid)
        print("ERROR: US10: ",hid," is under 14 years of age when he was married")
for wid,wmdt,wbdt in zip(wife_id,marr_date,wife_bd):
    age = age_at_marriage(wbdt,wmdt)
    if age < 14 and age>0:
        under_age.append(wid)
        print("ERROR: US10: ",wid," is under 14 years of age when she was married")
def check_age(id):
    if id in under_age:
        return "INVALID"
    else:
        return "VALID"
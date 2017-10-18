import sqlite3
import re
from datetime import datetime
HID = []
WID= []
HName = []
WName = []
div_date = []
marr_date = []
SP_ID = []
check_list = []
conn = sqlite3.connect('DATA.db')
cur = conn.cursor()
cur.execute("SELECT SPOUSE FROM INDIVIDUAL WHERE LENGTH(SPOUSE)>5")
rows = cur.fetchall()
for spid in rows:
    SP_ID = list(spid)
    SP_ID = SP_ID[0].split(',')
for spid in SP_ID:
    cur.execute("SELECT MARRIED,DIVORCED,HUSBAND_ID,HUSBAND_NAME,WIFE_ID,WIFE_NAME FROM FAMILY WHERE ID=?",(spid,))
    rows1 = cur.fetchall()
    for m,d,hid,hnm,wid,wnm in rows1:
        marr_date.append(re.sub(r'[^0-9a-zA-Z ]','',str(m)))
        div_date.append(re.sub(r'[^0-9a-zA-Z ]','',str(d)))
        HID.append(re.sub(r'[^@0-9a-zA-Z ]','',str(hid)))
        HName.append(re.sub(r'[^0-9a-zA-Z ]','',str(hnm)))
        WID.append(re.sub(r'[^@0-9a-zA-Z]','',str(wid)))
        WName.append(re.sub(r'[^0-9a-zA-Z ]','',str(wnm)))
if len(HID) != len(set(HID)):
    for p,id in enumerate(set(HID)):
        div = div_date[p]
        if div !="NA":
            # do something when there is divorce date for the individual
            print(div)
            mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
            mdt1 = datetime.date(mdt1)
            mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
            mdt2 = datetime.date(mdt2)
            div = datetime.strptime(str(div),"%d %b %Y")
            div = datetime.date(div)
            if mdt1<mdt2:
                end = mdt2
                start = mdt1
            else:
                end = mdt1
                start = mdt2
            if start<div<end:
                continue
            else:
                check_list.append(id)
                print("ERROR: US11: ID-",id,"is in a bigamous relationship!")
        else:
            mdt1 = datetime.strptime(str(marr_date[p]), "%d %b %Y")
            mdt1 = datetime.date(mdt1)
            mdt2 = datetime.strptime(str(marr_date[p + 1]), "%d %b %Y")
            mdt2 = datetime.date(mdt2)
            if mdt1<mdt2:
                pos = p
                end = mdt2
                start = mdt1
            else:
                pos = p+1
                end = mdt1
                start = mdt2
            cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?",(WID[pos],))
            rr = cur.fetchall()
            for d in rr:
                d = re.sub(r'[^0-9a-zA-Z ]','',str(d))
                if d!="NA":
                    d = datetime.strptime(str(d),"%d %b %Y")
                    d = datetime.date(d)
                    if start<d<end:
                        continue
                    else:
                        check_list.append(id)
                        print("ERROR: US11: ID-", id, "has bigamous relationship!")
                else:
                    print("ERROR: Insufficient data - The individual",id," may or may not have a bigamous relationship")
if len(WID) != len(set(WID)):
    for p,id in enumerate(set(WID)):
        div = div_date[p]
        if div !="NA":
            print(div)
            #do something when there is divorce date for the individual
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
            if mdt1<mdt2:
                pos = p
                end = mdt2
                start = mdt1
            else:
                pos = p+1
                end = mdt1
                start = mdt2
            cur.execute("SELECT DEATH FROM INDIVIDUAL WHERE ID=?",(HID[pos],))
            rr = cur.fetchall()
            for d in rr:
                d = re.sub(r'[^0-9a-zA-Z ]','',str(d))
                if d!="NA":
                    d = datetime.strptime(str(d),"%d %b %Y")
                    d = datetime.date(d)
                    if start<d<end:
                        continue
                        print("No individual is in a bigamous relationship!")
                    else:
                        check_list.append(id)
                        print("ERROR: US11: ID-", id, "has bigamous relationship!")
                else:
                    print("ERROR: Insufficient data - The individual",id,"may or may not have a bigamous relationship")

def check(i):
    print(check_list)
    if i in check_list:
        print("ERROR")
        return "ERROR"
    else:
        print("NO ERR")
        print("NO ERR")
        return "NO ERROR"

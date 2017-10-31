import sqlite3
import re

conn = sqlite3.connect("GEDCOM_DATA_US20.db")
conn.text_factory = str

result = conn.execute("SELECT ID,ALIVE,SPOUSE from INDIVIDUAL")
data = result.fetchall()

def us30():
    livingMarried = []
    for indi in data:
        indi_id = indi[0]
        alive = indi[1]
        spouse = indi[2]

        #print(indi_id+" "+alive+" "+spouse)
        
        if(spouse != 'NA' and alive == 'True'):
            livingMarried.append(indi_id)
    
    str = ""
    for id in livingMarried:
        str += id+" " 

    print("US30 : List of living married is : "+str) 
    
                


us30()
        

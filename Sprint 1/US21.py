# Author: Pranit Kulkarni

import sqlite3

conn = sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str

query1 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT HUSBAND_ID FROM FAMILY)"

result1 = conn.execute(query1)

husbands = result1.fetchall()

#husbandsData = {}   # Creating new dictionary

for row in husbands:
    if row[1] != "M":
        name = row[0].replace("/","")
        print("Husband "+name+" is not Male")
    #husbandsData[row[0].replace("/","")] = row[1]   # For Husband: Save name and gender from each row of the result
    #print(row)



query2 = "SELECT NAME, GENDER FROM INDIVIDUAL WHERE ID IN (SELECT WIFE_ID FROM FAMILY)"

result2 = conn.execute(query2)

wives = result2.fetchall()

#print("------------------")
#wivesData = {}  # Creating new dictionary

for row in wives:
    
    if row[1] != "F":
        name = row[0].replace("/","")
        print("Wife "+name+" is not female")
    #wivesData[row[0].replace("/","")] = row[1]  # For WIFE: Save name and gender from each row of the result
    #print(row)




conn.close()
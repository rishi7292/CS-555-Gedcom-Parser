# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:36:43 2017

@author: rishi
"""
import sqlite3
conn=sqlite3.connect('DATA.db')
conn.text_factory = str
print "Executing the Userstory 31 => "
def US31():
    Result_query="select ID,name,age from INDIVIDUAL where spouse='NA' and age>30 and death='NA'"
    Final_result=conn.execute(Result_query)
    Final_value=Final_result.fetchall()
    for Each_row in Final_value:
        print "ERROR: US31: "+Each_row[1].replace("/"," ")+"is single and alive and has a age of",Each_row[2]," which is more than 30"
US31()

def check(age):
    if(age>30):
        return True
    else:
        return False
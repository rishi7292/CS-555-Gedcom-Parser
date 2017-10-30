# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 00:56:43 2017

@author: rishi
"""
import sqlite3
conn=sqlite3.connect('DATA.db')
conn.text_factory = str
print "Executing the Userstory 23 => "
def US23():
    query="select distinct I1.name,I1.birthday from INDIVIDUAL as I1,INDIVIDUAL as I2 where I1.ID!=I2.ID and I1.name=I2.name and I1.birthday=I2.birthday"
    result=conn.execute(query)
    value=result.fetchall()
    
    for each_row in value:
        print "ERROR: US23:",each_row[0].replace("/"," "),"has birthday on",each_row[1]," and appears more than one time"
US23()

def check(name):
    new_query="select distinct I1.name,I1.birthday from INDIVIDUAL as I1,INDIVIDUAL as I2 where I1.ID!=I2.ID and I1.name=I2.name and I1.birthday=I2.birthday"
    new_result=conn.execute(new_query)
    new_value=new_result.fetchall()
    
    if(name in new_value):
        return True
    else:
        return False
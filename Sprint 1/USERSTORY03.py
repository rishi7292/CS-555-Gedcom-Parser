# -*- coding: utf-8 -*-
"""
Created on Mon Oct 02 14:41:56 2017

@author: rishi
"""
import sqlite3
conn=sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str
def Story03():
    query1="select NAME,AGE from INDIVIDUAL"

    result1=conn.execute(query1)

    value=result1.fetchall()
    first=value[0]
#def check(name):
    for row in value:
        if(row[1]<=0):
            print (row[0],"has an invalid age since birthday is after death day")
        else:
            print (row[0],"has a valid age of ",row[1])
Story03()
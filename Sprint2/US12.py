# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 17:30:31 2017

@author: rishi
"""
import sqlite3
from datetime import datetime


conn=sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str
print "Executing the Userstory 12 => "
def US12():
    query="SELECT I1.BIRTHDAY AS HUSBAND_BIRTHDAY, I2.BIRTHDAY AS WIFE_BIRTHDAY, I3.BIRTHDAY as CHILD_BIRTHDAY,F1.HUSBAND_NAME,F2.WIFE_NAME FROM INDIVIDUAL I1 INNER JOIN INDIVIDUAL I2 ON I1.ID <> I2.ID INNER JOIN INDIVIDUAL I3 ON I1.ID<>I3.ID AND I2.ID<> I3.ID INNER JOIN FAMILY F1 ON F1.HUSBAND_ID = I1.ID INNER JOIN FAMILY F2 ON F2.WIFE_ID=I2.ID INNER JOIN FAMILY F3 ON I3.CHILD=F3.ID WHERE F1.ID=F2.ID AND F3.ID=F1.ID"
    result1=conn.execute(query)
    value1=result1.fetchall()
    i=0
    date_format="%d %b %Y"
    for row in value1:
        first_row=value1[i]
        husband_birthday=datetime.strptime(first_row[0],date_format).date()
        
        wife_birthday=datetime.strptime(first_row[1],date_format).date()
        
        child_birthday=datetime.strptime(first_row[2],date_format).date()
        
        husband_child_diff=husband_birthday-child_birthday
        
        husband_child_yearsdiff=husband_child_diff.days/365
        
        wife_child_diff=husband_birthday-child_birthday
        
        wife_child_yearsdiff=wife_child_diff.days/365
        if((husband_child_yearsdiff>80) and (wife_child_yearsdiff>60)):
            print("ERROR :: US12 :: "+first_row[3].replace("/"," ")+" or "+first_row[4].replace("/"," ")+" have a child either more than 60 years younger than mother or more than 80 years younger than father")
        
        i+=1
US12()
def check(husband_age,son_age):
    if(husband_age-son_age<80):
        return True
    else:
        return False
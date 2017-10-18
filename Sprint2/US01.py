# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 13:54:20 2017

@author: rishi
"""
import sqlite3
import datetime
import time

conn=sqlite3.connect('GEDCOM_DATA.db')
conn.text_factory = str

def US01():
    current=datetime.datetime.now().date()
    print ("Current date is ::")
    print (current)
    query1="select NAME,BIRTHDAY,DEATH from INDIVIDUAL"
    result1=conn.execute(query1)
    value1=result1.fetchall()
    i=0
    date_format="%d %b %Y"
    for row in value1:
        first_row=value1[i]
        #print first_row
        a=datetime.datetime.strptime(first_row[1],'%d %b %Y').date()
        #print a
        if(first_row[2]=='NA'):
            pass
        else:
            c=datetime.datetime.strptime(first_row[2],'%d %b %Y').date()
            #c.strftime('%d %m %Y')
        #print c
        if(c=='NA'):
            pass
        elif(c!='NA' and (current<a or current<c)):
            
            print ("ERROR:: US01 :: ",first_row[1].replace("/"," ")," or ",first_row[2].replace("/"," ")+" is after the current date ")
        
        i+=1
        
    query2="select HUSBAND_NAME,WIFE_NAME,MARRIED,DIVORCED from FAMILY"
    result2=conn.execute(query2)
    value2=result2.fetchall()
    j=0
    e='NA'
    for row in value2:
        first_row=value2[j]
        d=datetime.datetime.strptime(first_row[2],'%d %b %Y').date()
        #print a
        if(first_row[3]=='NA'):
            pass
        else:
            e=datetime.datetime.strptime(first_row[3],'%d %b %Y').date()
         
        if(e=='NA'):
            pass
        elif(current<d or current<e):
            print ('ERROR:: US01 :: ",first_row[2].replace("/"," ")," or ",first_row[3].replace("/"," ")+" is after the current date')
        
        j+=1
US01()

def check(birthday,marriage_date):
    current_date=datetime.datetime.now().date()
    birthday=datetime.datetime.strptime(birthday,'%d %b %Y').date()
    d.strftime('%d %m %Y')
    marriage_date=datetime.datetime.strptime(marriage_date,'%d %b %Y').date()
    d.strftime('%d %m %Y')
    if(current_date>birthday or current_date>marriage_date):
        return True
    else:
        return False
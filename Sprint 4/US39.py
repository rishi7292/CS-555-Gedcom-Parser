# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 13:34:15 2017
"Database change required is: Changing Jon Snow and Monica Stark marriage date to 3rd december 2016"
@author: rishi
"""

import sqlite3
import datetime
conn=sqlite3.connect('DATA_Sprint4.db')
conn.text_factory = str
print "Executing the Userstory 39 => "
def US39():
    current_date=datetime.datetime.now().date()
    #print "Current Date is: ",current_date
    current_day=current_date.day
    current_month=current_date.month
    
    end_date = current_date + datetime.timedelta(days=30)
    #print "After 30 days the date is: ",end_date

    Result_query="select distinct F.Husband_name,F.wife_name,F.married from FAMILY as F,INDIVIDUAL as I where (F.husband_id=I.Id or F.wife_id=I.id) and I.death='NA' and F.married!='NA'"
    Final_result=conn.execute(Result_query)
    Final_value=Final_result.fetchall()
    
    for Each_row in Final_value:
        if(Each_row[2]=='NA'):
            pass
        else:
            converted_date=datetime.datetime.strptime(Each_row[2],'%d %b %Y').date()
            converted_day=converted_date.day
            converted_month=converted_date.month
            
            if(converted_month-current_month==0 and converted_day-current_day>0):
                print "ERROR: US39: ",Each_row[0].replace("/"," "),"and",Each_row[1].replace("/"," "),"have a upcoming marriage anniversary"
            elif(converted_month-current_month==1 and (converted_day-current_day>0 or current_day-converted_day>0)):
                print "ERROR: US39: ",Each_row[0].replace("/"," "),"and",Each_row[1].replace("/"," "),"have a upcoming marriage anniversary" 
US39()

def check(Anniversary_date):
    current_date=datetime.datetime.now().date()
    current_day=current_date.day
    current_month=current_date.month
    converted_date=datetime.datetime.strptime(Anniversary_date,'%d %b %Y').date()
    converted_day=converted_date.day
    converted_month=converted_date.month
            
    if(converted_month-current_month==0 and converted_day-current_day>0):
        return True
    elif(converted_month-current_month==1 and (converted_day-current_day>0 or current_day-converted_day>0)):
        return True
    else:
        return False
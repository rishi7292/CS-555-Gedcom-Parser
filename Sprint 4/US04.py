# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 14:26:24 2017
"Database change required is: Changing John Snow and Monica Stark divorce date to 4th November 2016"
@author: rishi
"""

import sqlite3
import datetime
conn=sqlite3.connect('DATA_Sprint4.db')
conn.text_factory = str
print "Executing the Userstory 04 => "
def US04():
    Result_query="select husband_name,wife_name,married,divorced from FAMILY"
    Final_result=conn.execute(Result_query)
    Final_value=Final_result.fetchall()
    
    for Each_row in Final_value:
        if(Each_row[2]=='NA' or Each_row[3]=='NA'):
            pass
        else:
            Marriage_date=datetime.datetime.strptime(Each_row[2],'%d %b %Y').date()
            Divorce_date=datetime.datetime.strptime(Each_row[3],'%d %b %Y').date()

            if(Divorce_date<Marriage_date):
                print"ERROR: US04:",Each_row[0].replace("/"," "),"and",Each_row[1].replace("/"," "),"have a Divorce date before their Marriage date"

US04()

def check(marriage_date,divorce_date):
    marriage_date=datetime.datetime.strptime(marriage_date,"%d %b %Y")
    divorce_date=datetime.datetime.strptime(divorce_date,"%d %b %Y")
    if(marriage_date>divorce_date):
        return True
    else:
        return False
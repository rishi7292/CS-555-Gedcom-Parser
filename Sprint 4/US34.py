# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 03:58:49 2017

US34 : List all couples who were married 
when the older spouse was more than twice as old as the younger spouse

@author: shreyas
"""

import sqlite3
import datetime
conn=sqlite3.connect('Sprint4.db')
conn.text_factory = str
print "Executing the Userstory 34 => "
def US34():
    Result_query="select Husband_name,wife_name,married,I1.birthday as husband_birthday,I2.birthday as wife_birthday from FAMILY as F,INDIVIDUAL as I1,INDIVIDUAL as I2 where I1.ID=F.husband_id and I2.ID=F.wife_id"
    Final_result=conn.execute(Result_query)
    Final_value=Final_result.fetchall()
    
    for Each_row in Final_value:
        if(Each_row[2]=='NA' or Each_row[3]=='NA' or Each_row[3]=='NA'):
            pass
        else:
            Marriage_date=datetime.datetime.strptime(Each_row[2],'%d %b %Y').date()
            Husband_birthdate=datetime.datetime.strptime(Each_row[3],'%d %b %Y').date()
            Wife_birthdate=datetime.datetime.strptime(Each_row[4],'%d %b %Y').date()
            
            
            husband_age= Marriage_date-Husband_birthdate
            wife_age=Marriage_date-Wife_birthdate
            
            if(husband_age>2*wife_age or wife_age>2*husband_age):
                print"ERROR: US34:",Each_row[0].replace("/","")," or ",Each_row[1].replace("/","")," have a greater age difference"

US34()
gedFile = open("D:/Stevens/3rd Sem/Agile/Assignments/Project02/proj02test.ged","r")

#List for Level 0 tags
level0tags = ["HEAD","TRLR","NOTE"] 

#List for Level 1 tags
level1tags = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV"]

#For Level 2 DATE is the only valid tag
level2tags = "DATE" 

#Special Level 0 tags with Id
validtags0 = ["INDI","FAM"]


#This will contains words read from every line.
myList = []


#Start reading file line  by line
for line in gedFile:
    print("-->"+line)
    myList = line.strip().split(" ")
    level = myList[0]
    
    #Check for level 0 
    if level == "0":
        if myList[1] in level0tags:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"Y"+"|"+" ".join(myList[2:]))
        elif myList[2] in validtags0:
            tag = myList[2]
            id = myList[1]
            print("<--"+level+"|"+tag+"|"+"Y"+"|"+id)
        else:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"N"+"|"+" ".join(myList[2:]))
    
    #Check for level 1
    if level == "1":
        if myList[1] in level1tags:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"Y"+"|"+" ".join(myList[2:]))
        else:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"N"+"|"+" ".join(myList[2:]))
    
    #Check for level 2
    if level == "2":
        if myList[1] == level2tags:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"Y"+"|"+" ".join(myList[2:]))
        else:
            tag = myList[1]
            print("<--"+level+"|"+tag+"|"+"N"+"|"+" ".join(myList[2:]))
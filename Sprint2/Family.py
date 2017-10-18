class Family:

    fam_id = ""
    birthdates = []

    def setFamId(self,id):
        self.fam_id = id

    def getFamId(self):
        return self.fam_id

    def setBirthdate(self,date):
        self.birthdates.append(date)

    def validateNoOfSiblings(self):

        for i in range(len(self.birthdates)):
            for j in range(i+1, len(self.birthdates)):
                if(self.birthdates[i] != self.birthdates[j]):
                    return False
        
        return True
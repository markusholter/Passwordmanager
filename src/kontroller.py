from brukeradministrasjon import Brukeradministrasjon
from passordadministrasjon import Passordadministrasjon

class Kontroller:
    def __init__(self, brukerfil):
        self.BRUKERFIL = brukerfil
        self.BA = Brukeradministrasjon()
        self.PA = Passordadministrasjon()
        self.user = None
        self.passordfil = None
        self.master_password = None

    def checkIfTaken(self, user):
        return self.BA.checkIfTaken(self.BRUKERFIL, user)
    
    def getUser(self, user, master_password):
        worked = self.BA.getUser(self.BRUKERFIL, user, master_password)

        if worked:
            self.user = user
            self.passordfil = user + ".txt"
            self.master_password = master_password
        
        return worked
    
    def createUser(self, user, master_password):
        self.BA.createUser(self.BRUKERFIL, user, master_password)

    def addPassword(self, name, username, newPassword):
        return self.PA.addPassword(self.passordfil, self.master_password, name, username, newPassword.encode())
    
    def getPassword(self, name):
        return self.PA.getPassword(self.passordfil, self.master_password, name)
    
    def getNamesAndUsernames(self, s=""):
       return self.PA.getNamesAndUsernames(self.passordfil, s)
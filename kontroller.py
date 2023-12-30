from brukeradministrasjon import Brukeradministrasjon
from passordadministrasjon import Passordadministrasjon

class Kontroller:
    def __init__(self, passordfil, brukerfil):
        self.PASSORDFIL = passordfil
        self.BRUKERFIL = brukerfil
        self.BA = Brukeradministrasjon()
        self.PA = Passordadministrasjon()
        self.user = None
        self.master_password = None

    def checkIfTaken(self, user):
        return self.BA.checkIfTaken(self.BRUKERFIL, user)
    
    def getUser(self, user, master_password):
        worked = self.BA.getUser(self.BRUKERFIL, user, master_password)

        if worked:
            self.user = user
            self.master_password = master_password
            print(user, master_password)
        
        return worked
    
    def createUser(self, user, master_password):
        self.BA.createUser(self.BRUKERFIL, user, master_password)
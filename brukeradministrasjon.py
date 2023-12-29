import os
from hashlib import sha256
from string import ascii_lowercase
from random import choice

LENSALT = 8

class Brukeradministrasjon:
    def getUser(self, brukerfil, user, passwd):    
        with open(brukerfil, "r") as f:
            for line in f:
                line = line.strip().split(",")
                if line[0] != user: continue

                salt = line[2]
                hpasswd = sha256((passwd + salt).encode()).hexdigest()
                
                if line[1] == hpasswd:
                    return True
                
        return False

    def checkIfTaken(self, brukerfil, user):
        with open(brukerfil, "r") as f:
            usernames = [name.strip().split(",")[0] for name in f.readlines()[1:]]
        return user in usernames

    def createUser(self, brukerfil, user, passwd):
        if not os.path.exists(brukerfil):
            with open(brukerfil, "w") as f:
                f.write("user,hpasswd,salt\n")

        salt = "".join(choice(ascii_lowercase) for _ in range(LENSALT))
        hpasswd = sha256((passwd + salt).encode()).hexdigest()

        with open(brukerfil, "a") as f:
            f.write(user + "," + hpasswd + "," + salt + "\n")
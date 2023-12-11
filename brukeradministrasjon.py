from kontrollerInterface import kontrollerInterface
import os
from hashlib import sha256
from string import ascii_lowercase
from random import choice

LENSALT = 8

class Brukeradministrasjon:
    def __init__(self, kontroller: kontrollerInterface) -> None:
        self.kont = kontroller

    def getUser(self, brukerfil):    
        user = self.kont.getInput("Type your username: ")
        passwd = self.kont.getInput("Type your password: ")

        with open(brukerfil, "r") as f:
            for line in f:
                line = line.strip().split(",")
                if line[0] != user: continue

                salt = line[2]
                hpasswd = sha256((passwd + salt).encode()).hexdigest()
                if line[1] != hpasswd:
                    self.kont.output("Wrong password! ")
                    return None, None
                
                if line[1] == hpasswd:
                    self.kont.output("You are logged in!")
                    return user, passwd
                
        self.kont.output("Found no username like that!")
        return None, None



    def createUser(self, brukerfil):
        if not os.path.exists(brukerfil):
            with open(brukerfil, "w") as f:
                f.write("user,hpasswd,salt\n")

        salt = "".join(choice(ascii_lowercase) for _ in range(LENSALT))

        with open(brukerfil, "r+") as f:
            usernames = [name.strip().split(",")[0] for name in f.readlines()[1:]]
            user = self.kont.getInput("Type your username: ")
            while user in usernames: 
                user = self.kont.getInput("That username is taken! Try another: ")

            passwd = self.kont.getInput("Type the password you want to use: ")
            hpasswd = sha256((passwd + salt).encode()).hexdigest()
            f.write(user + "," + hpasswd + "," + salt + "\n")

        self.kont.output("User added!")
        return user, passwd
from kontrollerInterface import kontrollerInterface
from brukeradministrasjon import Brukeradministrasjon
from passordadministrasjon import Passordadministrasjon
import sys

class Cli(kontrollerInterface):
    def __init__(self, filnavn, brukere) -> None:
        self.PASSORDFIL = filnavn
        self.BRUKERE = brukere
        self.BA = Brukeradministrasjon(self)
        self.PA = Passordadministrasjon(self)
        self.masterPasswd = ""
        self.loggInn()


    def drift(self):
        while True:
            print()
            print("What do you want to do?")
            print("0. Exit")
            print("1. Add new password")
            print("2. Get password")
            inp = input("Type the number here: ")
            print()
            if inp == "0": break
            elif inp == "1":
                self.addPassword()
            elif inp == "2":
                self.getPassword()
            else:
                print("Not a thing!")

    def addPassword(self):
        name = input("Write the name of the service: ")
        newPassword = input("Write the new password here: ").encode()
        if self.PA.addPassword(self.PASSORDFIL, self.masterPasswd, name, newPassword):
            print("Password for " + name + " is now added!")

    def getPassword(self):
        name = input("Write the name of the service: ")
        password = self.PA.getPassword(self.PASSORDFIL, self.masterPasswd, name)
        if password:
            print("Your password is:")
            print(password)
        else:
            print("No service with that name found!")


    def loggInn(self):
        print("Do you want to log in or create a user?")
        print("1. Create new user")
        print("*. Log in")
        inp = input("Type the number here: ")
        print()

        if inp == "1":
            self.createUser()
        else:
            self.getUser()

        self.drift()

    def createUser(self):
        user = input("Type your username: ")
        while self.BA.checkIfTaken(self.BRUKERE, user):
            user = input("That username is taken! Try another: ")
        
        password = input("Type the password you want to use: ")
        self.BA.createUser(self.BRUKERE, user, password)
        print("User added!")
        self.masterPasswd = password

    def getUser(self):
        user = input("Type your username: ")
        if not self.BA.checkIfTaken(self.BRUKERE, user):
            print("Found no username like that.")
            sys.exit(-1)
        
        password = input("Type your password: ")
        while not self.BA.getUser(self.BRUKERE, user, password):
            password = input("Wrong password! Try again: ")
        
        self.masterPasswd = password
        print("You are logged in!")

    #Override-metoder:

    def output(self, output):
        print(output)

    def getInput(self, question):
        return input(question)
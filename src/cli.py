from kontroller import Kontroller

import sys

class Cli():
    def __init__(self, brukere, kontroller: Kontroller) -> None:
        self.BRUKERE = brukere
        self.KONTROLLER = kontroller
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
        username = input("Write your username: ")
        newPassword = input("Write the new password here: ").encode()
        if self.KONTROLLER.addPassword(name, username, newPassword):
            print("Password for " + name + " is now added!")

    def getPassword(self):
        name = input("Write the name of the service: ")
        password = self.KONTROLLER.getPassword(name)
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
            self.loggInn()
            print()
            return
        else:
            self.getUser()

        self.drift()

    def createUser(self):
        user = input("Type your username: ")
        while self.KONTROLLER.checkIfTaken(user):
            user = input("That username is taken! Try another: ")
        
        password = input("Type the password you want to use: ")
        self.KONTROLLER.createUser(user, password)
        print("User added!")
        self.masterPasswd = password
        self.passordfil = user + ".txt"

    def getUser(self):
        user = input("Type your username: ")
        if not self.KONTROLLER.checkIfTaken(user):
            print("Found no username like that.")
            sys.exit(-1)
        
        password = input("Type your password: ")
        while not self.KONTROLLER.getUser(user, password):
            password = input("Wrong password! Try again: ")
        
        self.masterPasswd = password
        print("You are logged in!")
        self.passordfil = user + ".txt"
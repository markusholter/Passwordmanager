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
            print("3. List all saved services")
            print("4. Delete a service")
            print("5. Edit a service")
            inp = input("Type the number here: ")
            print()
            if inp == "0": break
            elif inp == "1":
                self.addPassword()
            elif inp == "2":
                self.getPassword()
            elif inp == "3":
                self.listAllServices()
            elif inp == "4":
                self.deleteItem()
            elif inp == "5":
                self.editItem()
            else:
                print("Not a thing!")

    def addPassword(self):
        service = input("Write the name of the service: ")
        username = input("Write your username: ")
        newPassword = input("Write the new password here: ")
        if self.KONTROLLER.addPassword(service, username, newPassword):
            print("Password for " + service + " is now added!")

    def getPassword(self):
        service = input("Write the name of the service: ")
        password = self.KONTROLLER.getPassword(service)
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

    def listAllServices(self):
        services = self.KONTROLLER.getNamesAndUsernames()
        print("This is the format printed: service: username")
        for service in services:
            print(f"{service}: {services[service]}")

    def deleteItem(self):
        service = input("Name of the service you want to delete: ")
        self.KONTROLLER.deleteItem(service)
        print(f"{service} is deleted!")

    def editItem(self):
        print("What do you want to change?")
        print("1. Service name")
        print("2. Username")
        print("3. Password")
        edit = input("Type the number here: ")

        service = input("Type the name of service you want to change: ")
        change = input("Type the change: ")

        if edit == "1":
            status = self.KONTROLLER.editServicename(service, change)
        elif edit == "2":
            status = self.KONTROLLER.editUsername(service, change)
        elif edit == "3":
            status = self.KONTROLLER.editPassword(service, change)
        else:
            print("Not a thing!")
            return
        
        if status:
            print("Change completed!")
        else:
            print("Couldn't change!")
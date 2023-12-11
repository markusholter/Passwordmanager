from kontrollerInterface import kontrollerInterface
from brukeradministrasjon import Brukeradministrasjon
from passordadministrasjon import Passordadministrasjon

class Cli(kontrollerInterface):
    def __init__(self, filnavn, brukere) -> None:
        self.FILNAVN = filnavn
        self.BRUKERE = brukere
        self.BA = Brukeradministrasjon(self)
        self.PA = Passordadministrasjon(self)
        self.loggInn()


    def drift(self, masterPasswd):
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
                self.PA.addPassword(self.FILNAVN, masterPasswd)
            elif inp == "2":
                self.PA.getPassword(self.FILNAVN, masterPasswd)
            else:
                print("Not a thing!")



    def loggInn(self):
        print("Do you want to log in or create a user?")
        print("1. Create new user")
        print("*. Log in")
        inp = input("Type the number here: ")
        print()

        if inp == "1":
            user, password = self.BA.createUser(self.BRUKERE)
        else:
            user, password = self.BA.getUser(self.BRUKERE)

        if user == None: return

        self.drift(password)


    #Override-metoder:

    def output(self, output):
        print(output)

    def getInput(self, question):
        return input(question)
from hashlib import pbkdf2_hmac, sha256
from brukeradministrasjon import getUser, createUser
from passordadministrasjon import addPassword, getPassword


def drift(masterPasswd):
    while True:
        print("What do you want to do?")
        print("0. Exit")
        print("1. Add new password")
        print("2. Get password")
        inp = input("Type the number here: ")
        print()
        if inp == "0": break
        elif inp == "1":
            addPassword(FILNAVN, masterPasswd)
        elif inp == "2":
            getPassword(FILNAVN, masterPasswd)
        else:
            print("Not a thing!")



def loggInn():
    print("Do you want to log in or create a user?")
    print("1. Create new user")
    print("*. Log in")
    inp = input("Type the number here: ")
    print()

    if inp == "1":
        user, password = createUser(BRUKERE)
    else:
        user, password = getUser(BRUKERE)

    if user == None: return

    drift(password)
    

if __name__ == "__main__":
    FILNAVN = "Passord.txt"
    BRUKERE = "Users.txt"
    loggInn()
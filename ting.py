import os
from hashlib import pbkdf2_hmac, sha256

def addPassword():
    name = input("Write the name of the service: ")
    newPassword = input("Write the new password here: ")

    if not os.path.exists(FILNAVN):
        with open(FILNAVN, "w") as f:
            f.write("name,password\n")

    with open(FILNAVN, "a") as f:
        f.write(name + "," + newPassword + "\n")

    print("Password for " + name + " is now added!")
    print()

def getPassword():
    name = input("Write the name of the service: ")
    password = ""
    with open(FILNAVN, "r") as f:
        for line in f:
            line = line.strip().split(",")
            if line[0].lower() == name.lower():
                password = line[1]
                break
    
    if password == "":
        print("No service with that name found!")
    else:
        print("Your password is:\n", password)
    print()


def getUser():    
    user = input("Type your username: ")
    passwd = input("Type your password: ")
    hpasswd = sha256((passwd + user).encode()).hexdigest()

    with open(BRUKERE, "r") as f:
        for line in f:
            line = line.strip().split(",")
            if line[0] != user: continue
            if line[1] != hpasswd:
                print("Wrong password! ")
                return None, None
            
            if line[1] == hpasswd:
                print("You are logged in!\n")
                return user, passwd
            
    print("Found noe username like that!")
    return None, None



def createUser():
    if not os.path.exists(BRUKERE):
        with open(BRUKERE, "w") as f:
            f.write("user, hpasswd\n")

    user = input("Type your username: ")
    passwd = input("Type the password you want to use: ")
    hpasswd = sha256((passwd + user).encode()).hexdigest()

    with open(BRUKERE, "a") as f:
        f.write(user + "," + passwd + "\n")

    print("User added!\n")
    return user, passwd


def drift():
    while True:
        print("What do you want to do?")
        print("0. Exit")
        print("1. Add new password")
        print("2. Get password")
        inp = input("Type the number here: ")
        print()
        if inp == "0": break
        elif inp == "1":
            addPassword()
        elif inp == "2":
            getPassword()
        else:
            print("Not a thing!")



def main():
    print("Do you want to log in or create a user?")
    print("1. Create new user")
    print("*. Log in")
    inp = input("Type the number here: ")
    print()

    if inp == "1":
        user, password = createUser()
    else:
        user, password = getUser()

    if user == None: return

    drift()
    

if __name__ == "__main__":
    FILNAVN = "Passord.txt"
    BRUKERE = "Users.txt"
    main()
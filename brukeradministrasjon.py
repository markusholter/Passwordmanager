import os
from hashlib import sha256
def getUser(brukerfil):    
    user = input("Type your username: ")
    passwd = input("Type your password: ")
    hpasswd = sha256((passwd + user).encode()).hexdigest()

    with open(brukerfil, "r") as f:
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



def createUser(brukerfil):
    if not os.path.exists(brukerfil):
        with open(brukerfil, "w") as f:
            f.write("user, hpasswd\n")

    user = input("Type your username: ")
    passwd = input("Type the password you want to use: ")
    hpasswd = sha256((passwd + user).encode()).hexdigest()

    with open(brukerfil, "a") as f:
        f.write(user + "," + passwd + "\n")

    print("User added!\n")
    return user, passwd
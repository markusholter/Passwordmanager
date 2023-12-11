import os
from hashlib import sha256
from Crypto.Random import get_random_bytes
from string import ascii_lowercase
from random import choice

LENSALT = 8


def getUser(brukerfil):    
    user = input("Type your username: ")
    passwd = input("Type your password: ")

    with open(brukerfil, "r") as f:
        for line in f:
            line = line.strip().split(",")
            if line[0] != user: continue

            salt = line[2]
            hpasswd = sha256((passwd + salt).encode()).hexdigest()
            if line[1] != hpasswd:
                print("Wrong password! ")
                return None, None
            
            if line[1] == hpasswd:
                print("You are logged in!\n")
                return user, passwd
            
    print("Found no username like that!")
    return None, None



def createUser(brukerfil):
    if not os.path.exists(brukerfil):
        with open(brukerfil, "w") as f:
            f.write("user,hpasswd,salt\n")

    salt = "".join(choice(ascii_lowercase) for _ in range(LENSALT))

    with open(brukerfil, "r+") as f:
        usernames = [name.strip().split(",")[0] for name in f.readlines()[1:]]
        user = input("Type your username: ")
        while user in usernames: 
            user = input("That username is taken! Try another: ")

        passwd = input("Type the password you want to use: ")
        hpasswd = sha256((passwd + salt).encode()).hexdigest()
        f.write(user + "," + hpasswd + "," + salt + "\n")

    print("User added!\n")
    return user, passwd
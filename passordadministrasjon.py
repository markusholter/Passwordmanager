import os


def addPassword(passordfil):
    name = input("Write the name of the service: ")
    newPassword = input("Write the new password here: ")

    if not os.path.exists(passordfil):
        with open(passordfil, "w") as f:
            f.write("name,password\n")

    with open(passordfil, "a") as f:
        f.write(name + "," + newPassword + "\n")

    print("Password for " + name + " is now added!")
    print()

def getPassword(passordfil):
    name = input("Write the name of the service: ")
    password = ""
    with open(passordfil, "r") as f:
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
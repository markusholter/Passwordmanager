import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from base64 import b64decode, b64encode


def addPassword(passordfil, passwd):
    name = input("Write the name of the service: ")
    newPassword = input("Write the new password here: ").encode()

    if not os.path.exists(passordfil):
        with open(passordfil, "w") as f:
            f.write("name,password,tag,nonce,salt\n")

    salt = get_random_bytes(16) # Litt salt må til
    key = scrypt(passwd, salt, 16, 2**14, 8, 1) # Nøkkel som skal brukes til krypteringen av passordet
    cipher = AES.new(key, AES.MODE_EAX) # Cipher til å kryptere
    cipherpass, tag = cipher.encrypt_and_digest(newPassword) # Krypteringsdel

    # Konverterer ting til strenger for å kunne skrive til fil:
    cipherpass = b64encode(cipherpass).decode()
    tag = b64encode(tag).decode()
    nonce = b64encode(cipher.nonce).decode()
    salt = b64encode(salt).decode()

    with open(passordfil, "a") as f:
        f.write(name + "," + cipherpass + "," + tag + "," + nonce + "," + salt + "\n")

    print("Password for " + name + " is now added!")
    print()


def getPassword(passordfil, masterPasswd):
    name = input("Write the name of the service: ")
    password = ""
    with open(passordfil, "r") as f:
        for line in f:
            line = line.strip().split(",")
            if line[0].lower() == name.lower():
                password, tag, nonce, salt = [x for x in line[1:]]
                break
    
    if password == "":
        print("No service with that name found!")
        return
    
    # Konverterer til bytes:
    password = b64decode(password.encode())
    tag = b64decode(tag.encode())
    nonce = b64decode(nonce.encode())
    salt = b64decode(salt.encode())
    
    key = scrypt(masterPasswd, salt, 16, 2**14, 8, 1)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    password = cipher.decrypt_and_verify(password, tag)


    print("Your password is:")
    print(password)
    print()
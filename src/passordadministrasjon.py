import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from base64 import b64decode, b64encode

class Passordadministrasjon:

    def addPassword(self, passordfil, master_password, service, username, new_password):

        if not os.path.exists(passordfil):
            with open(passordfil, "w") as f:
                f.write("service,username,password,tag,nonce,salt\n")

        cipherpass, tag, nonce, salt = self.encrypt(master_password, new_password)

        with open(passordfil, "a") as f:
            f.write(service + "," + username + "," + cipherpass + "," + tag + "," + nonce + "," + salt + "\n")

        return True


    def encrypt(self, master_password, new_password):
        salt = get_random_bytes(16) # Litt salt må til
        key = scrypt(master_password, salt, 16, 2**14, 8, 1) # Nøkkel som skal brukes til krypteringen av passordet
        cipher = AES.new(key, AES.MODE_EAX) # Cipher til å kryptere
        cipherpass, tag = cipher.encrypt_and_digest(new_password) # Krypteringsdel

        # Konverterer ting til strenger for å kunne skrive til fil:
        cipherpass = b64encode(cipherpass).decode()
        tag = b64encode(tag).decode()
        nonce = b64encode(cipher.nonce).decode()
        salt = b64encode(salt).decode()

        return cipherpass, tag, nonce, salt


    def getPassword(self, passordfil, master_password, service):
        password = ""
        with open(passordfil, "r") as f:
            for line in f:
                line = line.strip().split(",")
                if line[0].lower() == service.lower():
                    username, password, tag, nonce, salt = [x for x in line[1:]]
                    break
        
        if not password:
            return False
        
        # Konverterer til bytes:
        password = b64decode(password.encode())
        tag = b64decode(tag.encode())
        nonce = b64decode(nonce.encode())
        salt = b64decode(salt.encode())
        
        key = scrypt(master_password, salt, 16, 2**14, 8, 1)
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        password = cipher.decrypt_and_verify(password, tag).decode()


        return password
    

    def getNamesAndUsernames(self, passordfil, search) -> dict:
        if not os.path.exists(passordfil):
            return {}
        names = {}

        with open(passordfil, "r") as f:
            f.readline()
            for line in f:
                line = line.strip().split(",")
                if search not in line[0]: continue
                names[line[0]] = line[1]

        return names
    
    def deleteItem(self, passordfil, service):
        if not os.path.exists(passordfil):
            return
        
        with open(passordfil, "r") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if lines[i].strip().split(",")[0] != service: 
                continue
            lines.pop(i)
            break

        with open(passordfil, "w") as f:
            f.writelines(lines)

    def editItem(self, passordfil, service, change, index) -> bool:
        if not os.path.exists(passordfil):
            return False
        
        with open(passordfil, "r") as f:
            lines = f.readlines()

        for i in range(1, len(lines)):
            line = lines[i].split(",")
            if line[0] != service:
                continue
            line[index] = change
            lines[i] = ",".join(line)
            with open(passordfil, "w") as f:
                f.writelines(lines)
            return True
        
        return False
    
    def editPassword(self, passordfil, service, master_password, new_password):
        if not os.path.exists(passordfil):
            return False
        
        cipherpass, tag, nonce, salt = self.encrypt(master_password, new_password)

        with open(passordfil, "r") as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].split(",")
            if line[0] != service:
                continue
            for _ in range(len(line[2:])):
                line.pop()

            line.extend([cipherpass, tag, nonce, salt + "\n"])
            lines[i] = ",".join(line)
            with open(passordfil, "w") as f:
                f.writelines(lines)
            return True
        
        return False
# This is to generate the strong password for given length!!!!!
from cryptography.fernet import Fernet
import string
import random
import flask
import cryptography

class PasswordManagement: 
    def __init__(self) -> None:
        self.key=None
        self.Path=None
        self.password_file=None
        self.passwordMgr_dict={}

# This method will generate the random passord for given length
    def generatePass(self,passKey,passLength):
        lowerLetters=list(string.ascii_lowercase)
        upperLetters=list(string.ascii_uppercase)
        specialLetters=list(string.punctuation)
        numericLetters=list(string.digits)
        allLetters=lowerLetters+upperLetters+specialLetters+numericLetters
        strongPass=''.join(random.choice(allLetters) for _ in range(passLength))
        self.addPass(passKey,strongPass)
        
# This method is used to store encrypted password
# This method is used to create a key
    def createKey(self,path):
        key=Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(key)
# This method is used to load a key
    def loadKey(self,path):
        with open(path,"rb") as f:
            self.key=f.read()
# This method will create the password file to store the passwords:
    def createPassFile(self, path, intial_values=None):
        self.password_file=path
        if intial_values is not None:
            for key, value in intial_values.items():
                self.addPass(key,value)
# This method will be used to load the dictionary with passwords and keys form the given file.
    def loadPass(self,path):
        self.password_file=path
        with open(path, "r") as f:
            for line in f:
                passKey, encryptedPass= line.split(":")
                self.passwordMgr_dict[passKey]= Fernet(self.key).decrypt(encryptedPass.encode()).decode()
# This method will be use to add the pass with Key in pass file
    def addPass(self, passKey, genPass):
        self.passwordMgr_dict[passKey]=genPass
        if self.password_file is not None:
            with open(self.password_file, "a+") as f:
                encryptedPass=Fernet(self.key).encrypt(genPass.encode())
                f.write(passKey + ":" + encryptedPass.decode() + "\n") 
# This method will be used to get pass for provided key
    def getPass(self,keyPass):
        return self.passwordMgr_dict[keyPass]


def main():
    pm=PasswordManagement
    print (""" Select your choice?
           1. Generate New Password with passKey provided
           2. Add Existing Password
           3. Get a Password
           4. Exit
    """)
    done =False
    while not done:
        choice=input("Enter your choice: ")
        if choice=="1":
            num = int(input("Enter the length to generate: "))
            key=input("Provide the key to store the passoward")
            pm.generatePass(num,key)
        if choice=="2":
            key=input("Provide the key to store the passoward")
            keyPass=input("Provide the existing password to be stored")
            pm.addPass(key,keyPass)
        if choice=="3":
            getPass=pm.getPass()
            print(getPass)
        if choice=="f":
            exit()


if __name__=="__main__": 
    main()
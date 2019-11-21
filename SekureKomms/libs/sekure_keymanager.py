from .sekurelib import SekureLib
from Crypto.PublicKey import RSA
import time, os
from base64 import b64encode,b64decode

class SKKM:
    def __init__(self,terminal):
        self.sklib = SekureLib()
        self.term = terminal
        self.maxOtpUse = 5

    def initMenu(self):
        self.menuObj = {
        "1":{"function":self.getOTPs,"text":"1. View OTP Keys"},
        "2":{"function":self.newOTP,"text":"2. Create New OTP"},
        "3":{"function":self.expireOTP,"text":"3. Expire OTP"},
        "4":{"function":self.importOTP,"text":"4. Import OTP"},
        "5":{"function":self.exportOTP,"text":"5. Export OTP"},
        "6":{"function":self.purgeOTP,"text":"6. Purge Expired Keys"},
        "7":{"function":self.regenerateRSA,"text":"7. Regenerate RSA Keys"},
        "8":{"function":self.changeMasterPass,"text":"8. Change Master Password"},
        "9":{"function":print,"text":"9. Quit and return to main menu"}
        }

    def menu(self):
        print(self.term.clear)
        self.initMenu()
        for i in range(len(self.menuObj)):
            i = str(i+1)
            print(self.menuObj[i]['text'])
        choice = input(": ")
        if choice in self.menuObj:
            self.menuObj[choice]['function']()
        else:
            self.menu()

    def getOTPs(self):
        for key in self._OTPKeys:
            print("ID: %s Uses left: %s"%(key['id'],key['uses']))
            print("Key hash: %s"%self.sklib.generateMD5(key['key']))
        input("Press enter to return to menu")
        self.menu()

    def newOTP(self):
        tempotp = self.sklib.generateOTPKey()
        id = 0
        if len(self._OTPKeys) > 0:
            print(self._OTPKeys[-1]['id'])
            id = int(self._OTPKeys[-1]['id'])+1
        else:
            id = 1
        self._OTPKeys.append({'id':id,'key':tempotp,'uses':self.maxOtpUse})
        # self.saveKeyDatabase()
        self.menu()

    def expireOTP(self):
        key = self.selectOTP()
        for i in range(len(self._OTPKeys)):
            tempkey = self._OTPKeys[i]
            if tempkey['id'] == key['id']:
                self._OTPKeys[i]['uses']=0
                break
        self.menu()

    def importOTP(self):
        self.menu()

    def exportOTP(self):
        import json
        key = self.selectOTP()
        filename = self.sklib.generateMD5(key['key'])
        filename = filename + ".key"
        exportpath = "./client/otpexport/"+filename
        key = json.dumps(key)
        passw = self.getUserPassword()
        export = self.sklib.AESEncrypt(key,passw)
        del passw
        fd = open(exportpath,'w+')
        fd.write(export)
        fd.close()
        self.menu()

    def purgeOTP(self):
        self.menu()

    def selectOTP(self):
        print(self.term.clear())
        print("Select a key...\n")
        for otp in self._OTPKeys:
            print("ID: %s  Uses: %s"%(otp['id'],otp['uses']))
        choice = input(": ")
        choice = int(choice)
        key = None
        for i in range(len(self._OTPKeys)):
            thiskey = self._OTPKeys[i]
            print("Key ID:",thiskey['id'],"Index",i)
            if thiskey['id'] == choice:
                key = thiskey
        return key

    def regenerateRSA(self):
        self._keypair = self.sklib.generateRSAKeyPair()
        self._privatekey = self._keypair[0]
        self._publickey = self._keypair[1]
        self.saveKeyDatabase()
        self.menu()

    def changeMasterPass(self):
        self.saveKeyDatabase()
        self.menu()

    def generateDatabase(self):
        self._keypair = self.sklib.generateRSAKeyPair()
        self._privatekey = self._keypair[0]
        self._publickey = self._keypair[1]
        self._clientid = self.sklib.generateUUID()
        self._HMACSecret = self.sklib.generateHMACSecret()
        self._OTPKeys = []
        self._keydatabase = {
            'clientid':self._clientid,
            'privatekey':self._privatekey,
            'publickey':self._publickey,
            'HMACSecret':self._HMACSecret,
            'OTPKeys': self._OTPKeys
        }

    def loadKeyDatabase(self,database):
        import pickle
        import json
        self.keyfile = database
        if not os.path.exists(database):
            raise Exception('Monkey')
        for attempt in range(3):
            print("%s tries left."%(3-attempt))
            try:
                dbfile = open(database,'r+')
                db = dbfile.read()
                passw = self.getUserPassword()
                db = self.sklib.AESDecrypt(db,passw)
                self._keydatabase = json.loads(db)
                self._clientid = self._keydatabase['clientid']
                self._privatekey = self.importRSAKey(self._keydatabase['privatekey'])
                self._publickey = self.importRSAKey(self._keydatabase['publickey'])
                self._OTPKeys = self._keydatabase['OTPKeys']
                del passw
                dbfile.close()
                break
            except Exception as e:
                if attempt == 2:
                    print(e)
                    exit(0)
                else:
                    print('Incorrect encryption key.\n')

    def saveKeyDatabase(self):
        import pickle
        import json
        exportdb = {}
        exportdb['privatekey'] = self.exportRSAKey('private')
        exportdb['publickey'] = self.exportRSAKey()
        exportdb['clientid'] = self._keydatabase['clientid']
        exportdb['HMACSecret'] = self._keydatabase['HMACSecret']
        exportdb['OTPKeys'] = self._OTPKeys
        dbfile = open(self.keyfile,'w+')
        passw = self.getMasterPassword()
        db = json.dumps(exportdb)
        db = self.sklib.AESEncrypt(db,passw)
        del passw
        dbfile.write(db)
        dbfile.close()

    def importRemoteRSAPublic(self,key):
        key = b64decode(key)
        self._remotePublic = RSA.import_key(key)

    def importRSAKey(self,key):
        key = b64decode(key).decode()
        return RSA.import_key(key)

    def exportRSAKey(self,disposition='public'):
        privatekey = self._privatekey.exportKey()
        publickey = self._publickey.exportKey()
        if disposition == 'private':
            return b64encode(privatekey).decode()
        return b64encode(publickey).decode()

    def setSessionAESKey(self,key):
        self._sessionaeskey = key

    def getSessionAESKey(self):
        return self._sessionaeskey

    def getSessionOTP(self):
        return self._sessionOTP

    def setSessionOTP(self,sessionOTP):
        self._sessionOTP = sessionOTP

    def getClientID(self):
        return self._clientid

    def getRemotePublic(self):
        return self._remotePublic

    def getPublicKey(self):
        return self._publickey

    def getPrivateKey(self):
        return self._privatekey

    def generateKeypair(self):
        self._keypair = self.sklib.generateRSAKeyPair()
        self._privatekey = self._keypair[0]
        self._publickey = self._keypair[1]

    def getMasterPassword(self):
        import getpass
        # self.term.clear()
        # self.term.move(0, 0)
        passw = getpass.getpass("Encryption master password: ")
        return passw

    def getUserPassword(self):
        import getpass
        # self.term.clear()
        # self.term.move(0, 0)
        passw = getpass.getpass("Encryption password: ")
        return passw

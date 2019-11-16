from .sekurelib import SekureLib
from Crypto.PublicKey import RSA
import time, os
from base64 import b64encode,b64decode

class SKKM:
    def __init__(self,terminal):
        self.sklib = SekureLib()
        self.term = terminal

    def menu(self):
        print(self.term.clear)
        print("RSA Private: \n%s\n"%self._privatekey)
        print("RSA Public: \n%s\n"%self._publickey)
        print("RSA Private String: \n%s\n"%self.exportRSAKey('private'))
        print("RSA Public String: \n%s\n"%self.exportRSAKey())
        input("Press any key to continue...")

    def getKey(self,id):
        pass

    def getAllKeys(self):
        pass

    def generateDatabase(self):
        self._keypair = self.sklib.generateRSAKeyPair()
        self._privatekey = self._keypair[0]
        self._publickey = self._keypair[1]
        self._clientid = self.sklib.generateUUID()
        self._HMACSecret = self.sklib.generateHMACSecret()
        self._keydatabase = {
            'clientid':self._clientid,
            'privatekey':self._privatekey,
            'publickey':self._publickey,
            'HMACSecret':self._HMACSecret,
            'OTPKeys': []
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
        dbfile = open(self.keyfile,'w+')
        passw = self.getUserPassword()
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

    def generateKeypair(self):
        self._keypair = self.sklib.generateRSAKeyPair()
        self._privatekey = self._keypair[0]
        self._publickey = self._keypair[1]

    def getUserPassword(self):
        import getpass
        # self.term.clear()
        # self.term.move(0, 0)
        passw = getpass.getpass("Encryption password: ")
        return passw

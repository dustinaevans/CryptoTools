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
        print("RSA Private: \n%s\n"%self.privatekey)
        print("RSA Public: \n%s\n"%self.publickey)
        print("RSA Private String: \n%s\n"%self.exportRSAKey('private'))
        print("RSA Public String: \n%s\n"%self.exportRSAKey())
        input("Press any key to continue...")


    def getKey(self,id):
        pass

    def getAllKeys(self):
        pass

    def generateDatabase(self):
        self.keypair = self.sklib.generateRSAKeyPair()
        self.privatekey = self.keypair[0]
        self.publickey = self.keypair[1]
        self.clientid = self.sklib.generateUUID()
        self.HMACSecret = self.sklib.generateHMACSecret()
        self.keydatabase = {
            'clientid':self.clientid,
            'privatekey':self.privatekey,
            'publickey':self.publickey,
            'HMACSecret':self.HMACSecret,
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
                self.keydatabase = json.loads(db)
                self.clientid = self.keydatabase['clientid']
                self.privatekey = self.importRSAKey(self.keydatabase['privatekey'])
                self.publickey = self.importRSAKey(self.keydatabase['publickey'])
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
        exportdb['clientid'] = self.keydatabase['clientid']
        exportdb['HMACSecret'] = self.keydatabase['HMACSecret']
        dbfile = open(self.keyfile,'w+')
        passw = self.getUserPassword()
        db = json.dumps(exportdb)
        db = self.sklib.AESEncrypt(db,passw)
        del passw
        dbfile.write(db)
        dbfile.close()

    def importRemoteRSAPublic(self,key):
        key = b64decode(key)
        self.remotePublic = RSA.import_key(key)

    def importRSAKey(self,key):
        key = b64decode(key).decode()
        return RSA.import_key(key)

    def exportRSAKey(self,disposition='public'):
        privatekey = self.privatekey.exportKey()
        publickey = self.publickey.exportKey()
        if disposition == 'private':
            return b64encode(privatekey).decode()
        return b64encode(publickey).decode()

    def getUserPassword(self):
        import getpass
        self.term.clear()
        self.term.move(0, 0)
        passw = getpass.getpass("Encryption password: ")
        return passw

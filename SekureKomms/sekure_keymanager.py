from sekurelib import SekureLib
import blessings

class SKKM:
    def __init__(self,terminal):
        self.sklib = SekureLib()
        self.term = terminal
    def menu(self):
        print("Key management menu")

    def getKey(self,id):
        pass

    def getAllKeys(self):
        pass

    def loadKeyDatabase(self,database):
        import pickle
        import json
        try:
            dbfile = open(database,'r+')
            db = dbfile.read()
            passw = self.getUserPassword()
            db = self.sklib.AESDecrypt(db,passw)
            self.keydatabase = json.loads(db)
            del passw
            dbfile.close()
        except Exception as e:
            print("Load keydatabase failed in function loadKeyDatabase() with -",e)

    def saveKeyDatabase(self):
        import pickle
        import json
        exportdb = {}
        exportdb['privatekey'] = str(self.privatekey)
        exportdb['publickey'] = str(self.publickey)
        exportdb['clientid'] = self.clientid
        exportdb['HMACSecret'] = self.HMACSecret
        dbfile = open(self.keyfile,'w+')
        passw = self.getUserPassword()
        db = json.dumps(exportdb)
        db = self.sklib.AESEncrypt(db,passw)
        print(db)
        del passw
        dbfile.write(db)
        dbfile.close()

    def getUserPassword(self):
        import getpass
        self.term.clear()
        self.term.move(0, 0)
        passw = getpass.getpass("Encryption password: ")
        return passw

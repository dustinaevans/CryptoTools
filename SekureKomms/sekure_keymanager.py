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
        for attempt in range(3):
            print("%s tries left."%(3-attempt))
            try:
                dbfile = open(database,'r+')
                db = dbfile.read()
                passw = self.getUserPassword()
                db = self.sklib.AESDecrypt(db,passw)
                self.keydatabase = json.loads(db)
                self.clientid = self.keydatabase['clientid']
                del passw
                dbfile.close()
                break
            except Exception as e:
                if attempt == 2:
                    exit(0)
                else:
                    print('Incorrect encryption key.\n')

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

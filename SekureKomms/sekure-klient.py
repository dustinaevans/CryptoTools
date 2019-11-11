from sekurelib import SekureLib

class SekureKlient:
    def __init__(self,keyfile):
        self.sklib = SekureLib()
        self.keyfile = keyfile
        self.keydatabase = None
        try:
            print("Trying to load database from file...")
            self.loadKeyDatabase(self.keyfile)
            print("DB loaded successfully.")
        except Exception as e:
            print("Failed to load database, generating new DB -",e)
            self.keypair = self.sklib.generateRSAKeyPair()
            self.privatekey = self.keypair[0]
            self.publickey = self.keypair[1]
            self.clientid = self.sklib.generateUUID()
            self.HMACSecret = self.sklib.generateHMACSecret()
            self.keydatabase = {
                'ClientID':self.clientid,
                'RSAPrivate':self.privatekey,
                'RSAPublic':self.publickey,
                'HMACSecret':self.HMACSecret,
                'OTPKeys': []
            }

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
        passw = getpass.getpass("Encryption password: ")
        return passw


sk = SekureKlient('./keybase.db')
sklib = SekureLib()
print(sk.keydatabase)
sk.saveKeyDatabase()
#sk.saveKeyDatabase('./keybase.db')
# key = sklib.generateOTPKey('asdf')
# ct = sklib.OTPEncrypt("help me obiwan kinobi, you're my only hope.",key)
# pt = sklib.OTPDecrypt(ct,key)
# print(pt)
# rsakeys = sklib.generateRSAKeyPair()
# rsa_ct = sklib.RSAEncrypt("help me obiwan kinobi, you're my only hope.",rsakeys[1])
# rsa_pt = sklib.RSADecrypt(rsa_ct,rsakeys[0])
# print(rsa_pt)
# print(sklib.generateAESKey(rsakeys[1]))
# aes_ct = sklib.AESEncrypt("asdf",'password')
# print(aes_ct)
# aes_pt = sklib.AESDecrypt(aes_ct,"password")
# print(aes_pt)
# print(sklib.generateHMACSecret())

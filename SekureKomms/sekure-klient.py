from sekurelib import SekureLib

class SekureKlient:
    def __init__(self,privatekey,keysdatabase):
        self.sklib = SekureLib()
        self.keypair = self.sklib.generateRSAKeyPair()
        self.privatekey = self.keypair[0]
        self.publickey = self.keypair[1]
        self.clientid = self.sklib.generateUUID()
        self.HMACSecret = self.sklib.generateHMACSecret()
        self.keydatabase = {
            'ClientID':self.clientid,
            'RSAPrivate':self.privatekey,
            'RSAPublic':self.publickey,
            'HMACSecret':self.HMACSecret
        }

    def getKey(self,id):
        pass

    def getAllKeys(self):
        pass

    def loadKeyDatabase(self,database):
        try:
            dbfile = open(database,'r+b')
            db = dbfile.read()
            passw = self.getUserPassword()
            self.keydatabase = self.sklib.AESDecrypt(db,passw)
            del passw
        except:
            pass

    def saveKeyFile(self,database):
        pass

    def getUserPassword(self):
        passw = str(input("Password: "))
        return passw


sk = SekureKlient(1,2)
sklib = SekureLib()
key = sklib.generateOTPKey('asdf')
ct = sklib.OTPEncrypt("help me obiwan kinobi, you're my only hope.",key)
pt = sklib.OTPDecrypt(ct,key)
print(pt)
rsakeys = sklib.generateRSAKeyPair()
rsa_ct = sklib.RSAEncrypt("help me obiwan kinobi, you're my only hope.",rsakeys[1])
rsa_pt = sklib.RSADecrypt(rsa_ct,rsakeys[0])
print(rsa_pt)
print(sklib.generateAESKey(rsakeys[1]))
aes_ct = sklib.AESEncrypt("asdf",'password')
print(aes_ct)
aes_pt = sklib.AESDecrypt(aes_ct,"password")
print(aes_pt)
print(sklib.generateHMACSecret())

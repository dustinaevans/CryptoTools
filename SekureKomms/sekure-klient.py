from sekurelib import SekureLib
from sekure_keymanager import SKKM
import blessings

class SekureKlient:
    def __init__(self,keyfile):
        self.term = blessings.Terminal()
        print(self.term.enter_fullscreen)
        self.sklib = SekureLib()
        self.skkm = SKKM(self.term)
        self.connected = False
        self.runvar = True
        self.keyfile = keyfile
        self.keydatabase = None
        self.term.clear()
        try:
            print("Trying to load database from file...")
            self.skkm.loadKeyDatabase(self.keyfile)
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
        self.run()
        print(self.term.exit_fullscreen)

    def keyManagementMenu(self):
        self.skkm.menu()

    def mainMenu(self):
        self.term.clear()
        self.term.move(0, 0)
        print("1. Connect to a server")
        print("2. View messages offline")
        print("3. Key Management")
        print("4. Quit")
        choice = input(": ")
        if choice == "1":
            server = input("Enter server address: ")
            port = input("Enter server port: ")
            self.connectToServer(server,port)
        elif choice == "2":
            self.getMessages()
        elif choice == "3":
            self.keyManagementMenu()
        elif choice == "4":
            self.runvar = False
        else:
            self.mainMenu()

    def connectedMenu(self):
        self.term.clear()
        self.term.move(0, 0)
        print("Connected to server...")
        print("1. View messages")
        print("2. Compose message")
        print("3. Delete message")
        print("4. Key management")
        print("5. Disconnect")
        return input(": ")

    def connectToServer(self,server,port):
        # TCP socket to server:port save connection in object attribute self.server
        print("Connecting to %s"%server)
        pass

    def getMessages(self):
        print("Get messages")
        # collect encrypted messages
        pass

    def run(self):
        while self.runvar:
            if not self.connected:
                self.mainMenu()
            else:
                self.connectedMenu()
        print("Quitting...")


sk = SekureKlient('./keybase.db')
sklib = SekureLib()
# print(sk.keydatabase)
# sk.saveKeyDatabase()
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

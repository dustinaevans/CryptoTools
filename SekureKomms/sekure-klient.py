from sekurelib import SekureLib
from sekure_keymanager import SKKM
import blessings, socket, json
from base64 import b64decode,b64encode

class SekureKlient:
    def __init__(self,keyfile):
        self.term = blessings.Terminal()
        print(self.term.enter_fullscreen)
        self.sklib = SekureLib()
        self.skkm = SKKM(self.term)
        self.connected = False
        self.socket = None
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

    # {
    #   'action':'new'|'del'|'getone'|'getall',
    #   'query':{'msgid':<messageID>}|{'usrid':<userID>},
    #   'message':{'msgid':<messageID>,'message':<message>}
    # }

    def getOfflineMessages(self):
        pass

    def getOneMessage(self):
        data = {
        'action':'getone',
        'query':{'messageid':'12345'},
        'message':''
        }
        recv = self.socket.sendall(data.encode())
        print(recv)

    def getAllMessages(self):
        # {"message": "eyd1c2VyaWQnOiAnMDUzZDJiMGYtMmE2My00MTZlLThjZWQtNDU1Mjc0Y2ZmM2JhJywgJ3JjcHQnOiAnMDUzZDJiMGYtMmE2My00MTZlLThjZWQtNDU1Mjc0Y2ZmM2JhJywgJ21lc3NhZ2UnOiAnYWUzYjgzOGI5NzA0ZGZlMDNjN2RhYThkNGZlMzJkOTQ6ZGIzNTM1OTY0MDk4MmY4ZDZjZDJjMDFhNGM0YTI5Y2QnfQ==",
        # "id": "568358dc-fce8-493f-b9a7-b65ca902172b",
        # "hash": "407a469d55da229617ed36f14c8c706eeda9e658771f9823b3b8e1f2fcf71367847b2917df71eab2c947e0da1ac10fb39c9a835afbb70bfcec23acaa08dd43ec\\n",
        # "length": "178"}
        data = {
        'userid':str(self.skkm.clientid),
        'action':'getall',
        'query':{},
        'message':''
        }
        self.socket.sendall(json.dumps(data).encode())
        messages = self.socket.recv(1024).decode()
        messages = json.loads(messages)
        for i in messages:
            message = b64decode(i['message']).decode().replace("\'","\"")
            message = json.loads(message)
            print("Message ID: %s"%i['id'])
            print("Sender: %s"%message['userid'])
            print("Length: %s"%len(message['message']))
            print()

    def deleteMessage(self):
        pass

    def userInput(self,inputmsg):
        print(inputmsg)
        usrinput = input(": ")
        return usrinput

    def newMessage(self):
        self.term.clear()
        self.term.move(0,0)
        rcpt = self.userInput("Who would you like to send to?")
        message = self.userInput("Enter a message up to 4096 bytes")
        passw = self.userInput('Enter an encryption password')
        data = {
        'userid':str(self.skkm.clientid),
        'rcpt': rcpt,
        'action':'new',
        'query':{},
        'message':self.sklib.AESEncrypt(message,passw) # Change to one time pad when the keymanager is working
        }
        self.socket.send(bytes(json.dumps(data),'utf8'))

    def sendMessage(self,message):
        pass

    def disconnect(self):
        try:
            self.socket.close()
        except:
            pass
        print("Disconnected...")
        self.connected=False

    def mainMenu(self):
        self.term.clear()
        self.term.move(0, 0)
        choice = self.userInput("Welcome back %s\n1. Connect to a server\n2. View messages offline\n3. Key Management\n4. Quit\n"%str(self.skkm.clientid))
        if choice == "1":
            server = input("Enter server address: ")
            port = input("Enter server port: ")
            self.connectToServer(server,port)
        elif choice == "2":
            self.getOfflineMessages()
        elif choice == "3":
            self.keyManagementMenu()
        elif choice == "4":
            self.runvar = False
        else:
            self.mainMenu()

    def connectedMenu(self):
        self.term.clear()
        self.term.move(0, 0)
        print("1. View messages")
        print("2. Compose message")
        print("3. Delete message")
        print("4. Key management")
        print("5. Disconnect")
        choice = input(": ")
        if choice == '1':
            self.getAllMessages()
        elif choice == '2':
            self.newMessage()
        elif choice == '3':
            self.deleteMessage()
        elif choice == '4':
            self.keyManagementMenu()
        elif choice == '5':
            self.disconnect()
        else:
            self.connectedMenu()

    def connectToServer(self,server,port):
        # TCP socket to server:port save connection in object attribute self.server
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Connecting to %s"%server)
        try:
            self.socket.connect((server,int(port)))
            self.connected = True
        except Exception as e:
            print("Could not connect. %s"%e)

    def run(self):
        while self.runvar:
            if not self.connected:
                self.mainMenu()
            else:
                self.connectedMenu()
        print("Quitting...")





sk = SekureKlient('./keybase.db')


# sklib = SekureLib()
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

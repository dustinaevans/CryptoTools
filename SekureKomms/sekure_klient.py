from libs.sekurelib import SekureLib
from libs.sekure_keymanager import SKKM
import blessings, socket, json, time
from base64 import b64decode,b64encode

# Tasks:
# Move all keyfile vars to SKKM
# Change connected menu items to use secure comms
# Implement SKKM Menu
# Implement download messages
# Implement offline message viewing

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
        self.initMainMenu()
        self.initConnectedMenu()
        print(self.term.clear)
        try:
            print("Trying to load database from file...")
            self.skkm.loadKeyDatabase(self.keyfile)
            self.spinnyThing()
            print("DB loaded successfully.")
            time.sleep(1)
            print(self.term.clear)
        except Exception as e:
            print("Failed to load database, generating new DB -",e)
            self.skkm.generateDatabase()
            self.skkm.saveKeyDatabase()
        self.run()
        print(self.term.exit_fullscreen)

    def run(self):
        while self.runvar:
            if not self.connected:
                self.mainMenu()
            else:
                self.connectedMenu()
        print("Quitting...")

    def spinnyThing(self):
        word = "Decrypted"
        print(self.term.clear)
        output = ""
        for i in word:
            output += i
            print(self.term.move(0,0))
            print(output)
            time.sleep(.2)


    def initMainMenu(self):
        self.mainMenuObj = {
        '1':{'function':self.connectToServer,'text':'1. Connect to a server'},
        '2':{'function':self.getOfflineMessages,'text':'2. View messages offline'},
        '3':{'function':self.keyManagementMenu,'text':'3. Key Management'},
        '4':{'function':self.stopRun,'text':'4. Quit'}
        }

    def mainMenu(self):
        print(self.term.clear)
        print("Welcome back %s"%str(self.skkm.clientid))
        for i in self.mainMenuObj:
            print(self.mainMenuObj[i]['text'])
        choice = self.userInput("")
        if choice in self.mainMenuObj:
            self.mainMenuObj[choice]['function']()
        else:
            self.mainMenu()

    def connectToServer(self):
        server = self.userInput("Enter server address")
        port = self.userInput("Enter server port")
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Connecting to %s"%server)
        try:
            self.socket.connect((server,int(port)))
            self.negotiateSecurity()
            self.connected = True
        except Exception as e:
            print("Could not connect. %s"%(e))
            time.sleep(2)

    def getOfflineMessages(self):
        pass

    def keyManagementMenu(self):
        self.skkm.menu()

    def stopRun(self):
        self.runvar = False

    # {
    #   'action':'new'|'del'|'getone'|'getall',
    #   'query':{'msgid':<messageID>}|{'usrid':<userID>},
    #   'message':{'msgid':<messageID>,'message':<message>}
    # }

    def initConnectedMenu(self):
        self.connectedMenuObj  = {
        '1': self.getAllMessages,
        '2': self.newMessage,
        '3': self.deleteMessage,
        '4': self.keyManagementMenu,
        '5': self.disconnect
        }

    def connectedMenu(self):
        choice = self.userInput("ClientID: %s\n1. View messages\n2. Compose message\n3. Delete message\n4. Key management\n5. Disconnect"%self.skkm.clientid,True)
        if choice in self.connectedMenuObj:
            self.connectedMenuObj[choice]()
        else:
            self.connectedMenu()

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
        self.sendToServerEncrypted(json.dumps(data))
        messages = self.recvFromServerEncrypted()
        messages = json.loads(messages)
        for i in messages:
            message = b64decode(i['message']).decode().replace("\'","\"")
            message = json.loads(message)
            print("Message ID: %s"%i['id'])
            print("Sender: %s"%message['userid'])
            print("Length: %s"%len(message['message']))
            print()
        input("Press any key to continue...")

    def deleteMessage(self):
        pass

    def userInput(self,inputmsg,newpage=False):
        if newpage:
            print(self.term.clear)
        print(inputmsg)
        usrinput = input(": ")
        return usrinput

    def newMessage(self):
        rcpt = self.userInput("Who would you like to send to?",True)
        message = self.userInput("Enter a message up to 4096 bytes")
        passw = self.userInput('Enter an encryption password')
        data = {
        'userid':str(self.skkm.clientid),
        'rcpt': rcpt,
        'action':'new',
        'query':{},
        'message':self.sklib.AESEncrypt(message,passw) # Change to one time pad when the keymanager is working
        }
        self.sendToServer(json.dumps(data))

    def disconnect(self):
        try:
            self.socket.close()
        except:
            pass
        print("Disconnected...")
        self.connected=False

    def negotiateSecurity(self):
        self.sendToServer('negotiateSecurity')
        self.sendToServer(self.skkm.exportRSAKey())
        self.remotepublic = self.skkm.importRemoteRSAPublic(self.recvFromServer())
        self.sessionaeskey = self.recvFromServer()
        self.sessionOTP = self.sklib.generateOTPKey(self.sklib.generateAESKey(self.skkm.publickey))
        self.sendToServer(self.sessionOTP)
        if self.skkm.remotePublic and self.sessionaeskey and self.sessionOTP:
            print("Communication security negotiated...")
        else:
            raise Exception('NegotiatSecurityException')

    def sendToServer(self,message):
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServer(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        return message

    def sendToServerEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.sessionOTP)
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServerEncrypted(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        message = self.sklib.OTPDecrypt(message,self.sessionOTP)
        return message



sk = SekureKlient('./client/keybase.db')


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
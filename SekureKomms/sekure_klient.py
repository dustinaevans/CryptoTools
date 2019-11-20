from libs.sekurelib import SekureLib
from libs.sekure_keymanager import SKKM
from libs.utility import Utility
import blessings, socket, json, time
from base64 import b64decode,b64encode
import art

# Tasks:
# Move all keyfile vars to SKKM
# Implement SKKM Menu
# Fix RSA encrypt and decrypt functions
# Add RSA encrypt/decrypt to negotiateSecurity
# Add killswitch

class SekureKlient:
    def __init__(self,keyfile):
        self.term = blessings.Terminal()
        print(self.term.enter_fullscreen)
        self.sklib = SekureLib()
        self.sklib.testSelf()
        self.skkm = SKKM(self.term)
        self.connected = False
        self.socket = None
        self.runvar = True
        self.keyfile = keyfile
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
        self.utility = Utility(self.socket,self.sklib,self.skkm)
        self.run()
        print(self.term.exit_fullscreen)

    def run(self):
        while self.runvar:
            try:
                if not self.connected:
                    self.mainMenu()
                else:
                    self.connectedMenu()
            except Exception as e:
                print(e)
                time.sleep(5)
        print("Quitting...")

    def spinnyThing(self):
        word = "Decrypted"
        print(self.term.clear)
        output = ""
        for i in word:
            output += i
            print(self.term.move(0,0))
            print(output)
            time.sleep(.1)

    def initMainMenu(self):
        self.mainMenuObj = {
        '1':{'function':self.connectToServer,'text':'1. Connect to a server'},
        '2':{'function':self.viewOfflineMessages,'text':'2. View messages offline'},
        '3':{'function':self.keyManagementMenu,'text':'3. Key Management'},
        '4':{'function':self.stopRun,'text':'4. Quit'}
        }

    def mainMenu(self):
        print(self.term.clear)
        print("https://veteransec.com/")
        print()
        art.randomArt()
        print("Welcome back %s"%str(self.skkm.getClientID()))
        for i in range(len(self.mainMenuObj)):
            i = str(i+1)
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
            self.utility.setSocket(self.socket)
            self.utility.clientNegotiateSecurity()
            self.connected = True
        except Exception as e:
            print("Could not connect. %s"%(e))
            time.sleep(2)

    def viewOfflineMessages(self):
        fd = open('./client/messages.msg','r')
        messagesObj = {}
        index = 1
        message = None
        choice = ""
        for line in fd:
            messagesObj[str(index)]=line
            index+=1
        while choice != 'q':
            print(self.term.clear)
            for i in range(len(messagesObj)):
                i = str(i+1)
                rawmessage = json.loads(messagesObj[i])
                message = b64decode(rawmessage['message']).decode().replace("\'","\"").strip()
                message = json.loads(message)
                print(i+'.')
                print("Message ID: %s"%rawmessage['id'])
                print("Sender: %s"%message['userid'])
                print("Length: %s"%len(message['message']))
                print()
            choice = self.userInput("Select a message to read. Enter q to go back.")
            if choice == 'q':
                pass
            else:
                print(self.term.clear)
                chosen = json.loads(messagesObj[choice])
                message = b64decode(chosen['message']).decode().replace("\'","\"").strip()
                message = json.loads(message)
                sender = message['userid']
                recipient = message['rcpt']
                ctmessage = message['message']
                for z in range(3):
                    key = self.skkm.getUserPassword()
                    try:
                        ptmessage = self.sklib.AESDecrypt(ctmessage,key)
                        id = chosen['id']
                        print(self.term.clear)
                        print("ID: %s"%id)
                        print("Sender: %s"%sender)
                        print("Recipient: %s"%recipient)
                        print("Message: %s"%ptmessage)
                        print()
                        input("Press enter to continue...")
                        break
                    except:
                        print('Incorrect password')

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
        '1': self.syncMessages,
        '2': self.newMessage,
        '3': self.deleteMessage,
        '4': self.keyManagementMenu,
        '5': self.disconnect
        }

    def connectedMenu(self):
        choice = self.userInput("ClientID: %s\n1. Sync messages\n2. Compose message\n3. Delete message\n4. Key management\n5. Disconnect"%self.skkm.getClientID(),True)
        if choice in self.connectedMenuObj:
            self.connectedMenuObj[choice]()
        else:
            self.connectedMenu()

    def syncMessages(self):
        # {"message": "eyd1c2VyaWQnOiAnMDUzZDJiMGYtMmE2My00MTZlLThjZWQtNDU1Mjc0Y2ZmM2JhJywgJ3JjcHQnOiAnMDUzZDJiMGYtMmE2My00MTZlLThjZWQtNDU1Mjc0Y2ZmM2JhJywgJ21lc3NhZ2UnOiAnYWUzYjgzOGI5NzA0ZGZlMDNjN2RhYThkNGZlMzJkOTQ6ZGIzNTM1OTY0MDk4MmY4ZDZjZDJjMDFhNGM0YTI5Y2QnfQ==",
        # "id": "568358dc-fce8-493f-b9a7-b65ca902172b",
        # "hash": "407a469d55da229617ed36f14c8c706eeda9e658771f9823b3b8e1f2fcf71367847b2917df71eab2c947e0da1ac10fb39c9a835afbb70bfcec23acaa08dd43ec\\n",
        # "length": "178"}
        data = {
        'userid':str(self.skkm.getClientID()),
        'action':'getall',
        'query':{},
        'message':''
        }
        self.utility.sendToServerEncrypted(json.dumps(data))
        print("Sent encrypted message")
        messages = self.utility.recvFromServerEncrypted()
        messages = json.loads(messages)
        newmessagecount = 0
        for rawmessage in messages:
            newmessagecount += self.saveMessage(rawmessage)
        print("Synced %s new messages."%newmessagecount)
        input("Press any key to continue...")

    def deleteMessage(self):
        data = {
        'userid':str(self.skkm.getClientID()),
        'action':'del',
        'query':{},
        'message':''
        }
        self.utility.sendToServerEncrypted(json.dumps(data))
        print(self.term.clear)
        print("All messages have been deleted from the server.")
        input("Press enter to continue...")

    def newMessage(self):
        rcpt = self.userInput("Who would you like to send to?",True)
        message = self.userInput("Enter a message up to 4096 bytes")
        passw = self.userInput('Enter an encryption password')
        data = {
        'userid':str(self.skkm.getClientID()),
        'rcpt': rcpt,
        'action':'new',
        'query':{},
        'message':self.sklib.AESEncrypt(message,passw) # Change to one time pad when the keymanager is working
        }
        self.utility.sendToServerEncrypted(json.dumps(data))

    def disconnect(self):
        try:
            self.socket.close()
        except:
            pass
        print("Disconnected...")
        self.connected=False

    def saveMessage(self,message):
        msgids = []
        msgfile = open('./client/messages.msg','r')
        newmessagecount = 0
        for line in msgfile:
            curmsg = json.loads(line)
            msgids.append(curmsg['id'])
        msgfile.close()
        msgfile = open('./client/messages.msg','a+')
        if message['id'] in msgids:
            pass
        else:
            msgfile.write(json.dumps(message)+'\n')
            newmessagecount += 1
        msgfile.close()
        return newmessagecount

    def userInput(self,inputmsg,newpage=False):
        if newpage:
            print(self.term.clear)
        print(inputmsg)
        usrinput = input(": ")
        return usrinput


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

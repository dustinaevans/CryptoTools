from libs.sekurelib import SekureLib
from libs.sekure_keymanager import SKKM
from libs.utility import Utility
import blessings, socket, json, time
from base64 import b64decode,b64encode
import art

# Tasks:
# Add a local delete function
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
            if not self.connected:
                self.mainMenu()
            else:
                self.connectedMenu()
            try:
                pass
            except Exception as e:
                print(e)
                time.sleep(5)
        print("Quitting...")

    def initMainMenu(self):
        self.mainMenuObj = {
        '1':{'function':self.connectToServer,'text':'1. Connect to a server'},
        '2':{'function':self.viewOfflineMessages,'text':'2. View messages offline'},
        '3':{'function':self.newMessage,'text':'3. Create new message'},
        '4':{'function':self.keyManagementMenu,'text':'4. Key Management'},
        '5':{'function':self.stopRun,'text':'5. Quit'}
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
        print("Official server: ec2-3-15-201-201.us-east-2.compute.amazonaws.com Port: 8080")
        server = self.userInput("Enter server address")
        port = self.userInput("Enter server port")
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Connecting to %s"%server)
        self.socket.connect((server,int(port)))
        self.utility.setSocket(self.socket)
        self.utility.clientNegotiateSecurity()
        self.connected = True
        try:
            pass
        except Exception as e:
            print("Could not connect. Exception: %s"%(e))
            time.sleep(2)

    def newMessage(self):
        rcpt = self.userInput("Who would you like to send to?",True)
        message = self.userInput("\nMessages over 4600 will be truncated.\nEnter a message up to 9000 characters.")
        message = message[:4600]
        passw = self.skkm.selectOTP()
        data = {
        'userid':str(self.skkm.getClientID()),
        'rcpt': rcpt,
        'action':'new',
        'query':{},
        'message':self.sklib.OTPEncrypt(message,passw)
        }
        self.skkm.decrementOTP(passw)
        del passw
        message = json.dumps(data)
        queue = open('./client/messages.queue','a+')
        queue.write(message+"\n")
        print("Message will be held in queue until you synchronize.")
        self.skkm.saveKeyDatabase()
        queue.close()

    def viewOfflineMessages(self):
        import re
        fd = open('./client/messages.msg','r')
        messagesObj = {}
        index = 1
        message = None
        choice = ""
        for line in fd:
            messagesObj[str(index)]=line
            index+=1
        fd.close()
        while choice != 'q':
            print(self.term.clear)
            if len(messagesObj) == 0:
                print("No messages...")
                input("Enter to continue")
                break
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
            choice = self.userInput("Select a message to read. Enter d and the number to delete a message. Enter q to go back.")
            if choice == 'q':
                break
            elif re.match(r'd[0-9]',choice):
                choice = choice[1:]
                if int(choice) > len(messagesObj):
                    continue
                tempmessage = json.loads(messagesObj.pop(choice))
                print(tempmessage['id'],"deleted.")
                if int(choice) < len(messagesObj)+1:
                    tempmessage = messagesObj.pop(str(len(messagesObj)+1))
                    messagesObj[str(choice)] = tempmessage
                fd = open('./client/messages.msg','w+')
                fd.close()
                fd = open('./client/messages.msg','a+')
                for i in messagesObj:
                    fd.write(messagesObj[i])
                input("Enter to continue")
                fd.close()
                continue
            elif choice not in messagesObj:
                continue
            else:
                pass
            print(self.term.clear)
            chosen = json.loads(messagesObj[choice])
            message = b64decode(chosen['message']).decode().replace("\'","\"").strip()
            message = json.loads(message)
            sender = message['userid']
            recipient = message['rcpt']
            ctmessage = message['message']
            for z in range(3):
                key = self.skkm.selectOTP()
                try:
                    ptmessage = self.sklib.OTPDecrypt(ctmessage,key)
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
        '2': self.deleteMessage,
        '3': self.keyManagementMenu,
        '4': self.disconnect
        }

    def connectedMenu(self):
        choice = self.userInput("ClientID: %s\n1. Sync messages\n2. Delete messages\n3. Key management\n4. Disconnect"%self.skkm.getClientID(),True)
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
        self.utility.sendEncrypted(json.dumps(data))
        newmessagecount = 0
        message = self.utility.recvEncrypted()
        while message != "FIN":
            newmessagecount += self.saveMessage(message)
            message = self.utility.recvEncrypted()
        queue = open('./client/messages.queue','r')
        item = queue.readline()
        messagessent = 0
        while item:
            self.utility.sendEncrypted(item)
            item = queue.readline()
            messagessent += 1
        queue = open('./client/messages.queue','w+')
        queue.write("")
        queue.close()
        print("Sent %s new messages."%messagessent)
        print("Downloaded %s new messages."%newmessagecount)
        input("Press any key to continue...")

    def deleteMessage(self):
        data = {
        'userid':str(self.skkm.getClientID()),
        'action':'del',
        'query':{},
        'message':''
        }
        self.utility.sendEncrypted(json.dumps(data))
        print(self.term.clear)
        print("All messages have been deleted from the server.")
        input("Press enter to continue...")

    def disconnect(self):
        try:
            self.socket.close()
        except:
            pass
        print("Disconnected...")
        self.connected=False

    def saveMessage(self,message):
        msgids = []
        newmessagecount = 0
        if len(json.loads(message)) == 0:
            pass
        else:
            msgfile = open('./client/messages.msg','r+')
            for line in msgfile:
                curmsg = json.loads(line)
                msgids.append(curmsg['id'])
            msgfile.close()
            msgfile = open('./client/messages.msg','a+')
            message = json.loads(message)
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

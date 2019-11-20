import socket
import threading
import json
from libs.utility import Utility
from libs.sekurelib import SekureLib
from libs.sekure_keymanager import SKKM
from base64 import b64encode,b64decode

# Tasks:
# Move all keyfile vars to SKKM specifically negotiateSecurity vars
# Change connected menu items to use secure comms

class ServerThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        self.token = "1234509876"
        self.spot = "init"
        self.socket = clientsocket
        self.sklib = SekureLib()
        self.term = None
        self.skkm = SKKM(self.term)
        self.utility = Utility(self.socket,self.sklib,self.skkm)
        self.clientAddress = clientAddress
        threading.Thread.__init__(self)
        self.skkm.generateKeypair()
        self.mode = 'insecure'
        print ("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", clientAddress)
        self.spot = "run"
        while True:
            try:
                if self.mode == 'insecure':
                    self.spot = "negotiateSecurity"
                    self.utility.serverNegotiateSecurity()
                    self.mode = 'secure'
                else:
                    self.spot = "Receiving encrypted data"
                    data = self.utility.recvEncrypted()
                    self.spot = "Run data processing"
                    print("Received encrypted")
                    print(data)
                    data = json.loads(data)
                    if data['action'] == 'new':
                        self.spot = "Run new"
                        self.newMessage(data)
                    elif data['action'] == 'getall':
                        self.spot = "Run getall"
                        print(self.spot)
                        self.getAllMessages(data)
                    elif data['action'] == 'del':
                        self.spot = "Run delete"
                        self.deleteMessage(data)
                    else:
                        print('No action selected')
            except Exception as e:
                print(self.spot,e)
                break
        print ("Client at ", clientAddress , " disconnected...")

    def newMessage(self,data):
        self.spot = 'newMessage'
        # {"userid": "053d2b0f-2a63-416e-8ced-455274cff3ba",
        # "rcpt": "dustine",
        # "action": "new",
        # "message": "e9e9c68fafae2341f3bd2ac1975ee054:8e1257e9c14ffbbbb65886bc29b35ecd869d8b38acb1bd74f8acf4f83f24998e"}
        del data['query']
        del data['action']
        fd = open('./server/%s.msg'%data['rcpt'],'a')
        id = str(self.sklib.generateUUID())
        message = b64encode(bytes(str(data),'utf8')).decode()
        messagelength = len(str(data))
        hash = self.sklib.generateSHA(id+message+str(messagelength))
        storedMessage = "%s.%s.%s.%s\n"%(id,message,messagelength,hash)
        fd.write(storedMessage)
        fd.close()

    def getAllMessages(self,data):
        import os
        self.spot = "getAllMessages"
        print(self.spot)
        fd = open('./server/%s.msg'%data['userid'],'r')
        print("Opened message file")
        messages = []
        try:
            print("Starting getall try clause")
            if os.stat('./server/%s.msg'%data['userid']).st_size == 0:
                self.utility.sendEncrypted(json.dumps({}))
                print("Sent empty message")
            else:
                for line in fd:
                    print("Line found")
                    if len(line) <= 1:
                        raise("EmptyLineException")
                    line = line.split('.')
                    message = {
                    'id':line[0],
                    'message':line[1],
                    'length':line[2],
                    'hash':line[3].strip()
                    }
                    messages.append(message)
                    print("Sending messages")
                    self.utility.sendEncrypted(json.dumps(messages))
                    print("Sent messages")
        except:
            print("Sending empty")
            self.utility.sendEncrypted(json.dumps([]))
            print("Sent empty")
        fd.close()

    def deleteMessage(self,data):
        self.spot = "deleteMessage"
        fd = open('./server/%s.msg'%data['userid'],'w')
        fd.write(self.sklib.generateOTPKey())
        fd.seek(0)
        fd.write("")

    def getToken(self):
        token = self.sklib.generateSHA(self.token)
        return token.hex()


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
server.listen(5)
while True:
    clientsock, clientAddress = server.accept()
    newthread = ServerThread(clientAddress, clientsock)
    newthread.start()

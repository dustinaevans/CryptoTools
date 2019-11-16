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
                    data = self.utility.recvFromClient()
                    if data == 'GET':
                        print("Attempted web connection")
                        for i in range(10):
                            self.utility.sendToClient(self.sklib.generateOTPKey())
                        self.utility.sendToClient('\r\n')
                else:
                    self.spot = "Receiving encrypted data"
                    data = self.utility.recvFromClientEncrypted()
                if data == 'negotiateSecurity':
                    self.negotiateSecurity()
                else:
                    self.spot = "Run data processing"
                    data = json.loads(data)
                    if data['action'] == 'new':
                        self.spot = "Run new"
                        self.newMessage(data)
                    elif data['action'] == 'getall':
                        self.spot = "Run getall"
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
        self.spot = "getAllMessages"
        fd = open('./server/%s.msg'%data['userid'],'r')
        messages = []
        try:
            for line in fd:
                line = line.split('.')
                message = {
                'id':line[0],
                'message':line[1],
                'length':line[2],
                'hash':line[3].strip()
                }
                messages.append(message)
                self.utility.sendToClientEncrypted(json.dumps(messages))
        except:
            self.utility.sendToClientEncrypted(json.dumps([]))

    def deleteMessage(self,data):
        self.spot = "deleteMessage"
        fd = open('./server/%s.msg'%data['userid'],'w')
        fd.write(self.sklib.generateOTPKey())
        fd.seek(0)
        fd.write("")

    def negotiateSecurity(self):
        self.spot = "negotiateSecurity"
        self.skkm.importRemoteRSAPublic(self.utility.recvFromClient())
        self.utility.sendToClient(self.skkm.exportRSAKey())
        self.skkm.setSessionAESKey(self.sklib.generateAESKey(self.skkm.getPublicKey()))
        self.utility.sendToClient(self.sklib.RSAEncrypt(self.skkm.getSessionAESKey(),self.skkm.getRemotePublic()))
        self.skkm.setSessionOTP(self.utility.recvFromClient())
        if self.skkm.getRemotePublic() and self.skkm.getSessionAESKey() and self.skkm.getSessionOTP():
            print("Security negotiated with client")
            self.mode = 'secure'
            self.spot = "Ending security negotiation"
        else:
            raise Exception('NegotiateSecurityException')



LOCALHOST = "0.0.0.0"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ServerThread(clientAddress, clientsock)
    newthread.start()

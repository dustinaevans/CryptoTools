import socket, threading, json, blessings
from libs.sekurelib import SekureLib
from libs.sekure_keymanager import SKKM
from base64 import b64encode,b64decode

# Tasks:
# Move all keyfile vars to SKKM
# Change connected menu items to use secure comms

class ServerThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        self.term = blessings.Terminal()
        self.sklib = SekureLib()
        self.clientAddress = clientAddress
        threading.Thread.__init__(self)
        self.socket = clientsocket
        self.skkm = SKKM(self.term)
        self.keypair = self.sklib.generateRSAKeyPair()
        self.mode = 'insecure'
        self.skkm.privatekey = self.keypair[0]
        self.skkm.publickey = self.keypair[1]
        self.privatekey = self.keypair[0]
        self.publickey = self.keypair[1]
        print ("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", clientAddress)
        while True:
            if self.mode == 'insecure':
                data = self.recvFromClient()
            else:
                data = self.recvFromClientEncrypted()
            if data == 'negotiateSecurity':
                self.negotiateSecurity()
            else:
                data = json.loads(data)
                if data['action'] == 'new':
                    self.newMessage(data)
                elif data['action'] == 'getone':
                    self.getOneMessage(data)
                elif data['action'] == 'getall':
                    self.getAllMessages(data)
                elif data['action'] == 'del':
                    self.deleteMessage(data)
                else:
                    print('No action selected')
        print ("Client at ", clientAddress , " disconnected...")

    def newMessage(self,data):
        # {"userid": "053d2b0f-2a63-416e-8ced-455274cff3ba", "rcpt": "dustine", "action": "new", "message": "e9e9c68fafae2341f3bd2ac1975ee054:8e1257e9c14ffbbbb65886bc29b35ecd869d8b38acb1bd74f8acf4f83f24998e"}
        del data['query']
        del data['action']
        fd = open('%s.msg'%data['rcpt'],'a')
        id = str(self.sklib.generateUUID())
        message = b64encode(bytes(str(data),'utf8')).decode()
        messagelength = len(str(data))
        hash = self.sklib.generateSHA(id+message+str(messagelength))
        storedMessage = "%s.%s.%s.%s\n"%(id,message,messagelength,hash)
        fd.write(storedMessage)
        fd.close()

    def getOneMessage(self,data):
        pass

    def getAllMessages(self,data):
        fd = open('%s.msg'%data['userid'],'r')
        messages = []
        for line in fd:
            line = line.split('.')
            message = {
            'id':line[0],
            'message':line[1],
            'length':line[2],
            'hash':line[3]
            }
            messages.append(message)
        self.sendToClientEncrypted(json.dumps(messages))
        # self.socket.send(bytes(json.dumps(messages),'utf8'))

    def deleteMessage(self,data):
        pass

    def recvFromClient(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        return message

    def sendToClient(self,message):
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def sendToClientEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.sessionOTP)
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromClientEncrypted(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        message = self.sklib.OTPDecrypt(message,self.sessionOTP)
        return message

    def negotiateSecurity(self):
        self.skkm.importRemoteRSAPublic(self.recvFromClient())
        self.sendToClient(self.skkm.exportRSAKey())
        self.sessionaeskey = self.sklib.generateAESKey(self.publickey)
        print("Session Key: %s"%self.sessionaeskey)
        self.sendToClient(self.sklib.RSAEncrypt(self.sessionaeskey,self.skkm.remotePublic))
        self.sessionOTP = self.recvFromClient()
        if self.skkm.remotePublic and self.sessionaeskey and self.sessionOTP:
            print("Security negotiated with client")
            self.mode = 'secure'
        else:
            raise Exception('NegotiatSecurityException')



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

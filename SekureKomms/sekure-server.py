import socket, threading, json
from sekurelib import SekureLib
from base64 import b64encode,b64decode

class ServerThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        self.sklib = SekureLib()
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

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
            messages.append(line) # Create json from line
        self.csocket.send(bytes(json.dumps(messages),'utf8'))

    def deleteMessage(self,data):
        pass

    def run(self):
        print("Connection from : ", clientAddress)
        while True:
            data = self.csocket.recv(8192)
            print(data.decode())
            data = json.loads(data.decode())
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
            #self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")



LOCALHOST = "127.0.0.1"
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

import socket, threading

class ServerThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)

    def newMessage(self,data):
        pass

    def getOneMessage(self,data):
        pass

    def getAllMessages(self,data):
        pass

    def deleteMessage(self,data):
        pass

    def run(self):
        print("Connection from : ", clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(8192)
            try:
                data = json.loads(data.decode())
                if msg['action'] == 'new':
                    newMessage(data)
                elif msg['action'] == 'getone':
                    getOneMessage(data)
                elif msg['action'] == 'getall':
                    getAllMessages(data)
                elif msg['action'] == 'del':
                    deleteMessage(data)
                else:
                    break
            except:
                break
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
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()

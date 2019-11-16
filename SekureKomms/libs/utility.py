class Utility:

    def __init__(self,socket,sklib,skkm):
        self.socket = socket
        self.sklib = sklib
        self.skkm = skkm

    def sendToServer(self,message):
        print("Unencrypted",len(message))
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromClient(self):
        length = self.socket.recv(4)
        if "GET " in length.decode():
            return "GET"
        length = int(length.decode())
        message = self.socket.recv(length)
        return message.decode()

    def sendToClient(self,message):
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServer(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        return message

    def sendToServerEncrypted(self,message):
        print("Encrypted",len(message))
        message = self.sklib.OTPEncrypt(message,self.skkm.getSessionOTP())
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromClientEncrypted(self):
        length = self.socket.recv(4)
        print(length)
        length = int(length.decode())
        message = self.socket.recv(length)
        message = message.decode()
        message = self.sklib.OTPDecrypt(message,self.skkm.getSessionOTP())
        return message

    def sendToClientEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.skkm.getSessionOTP())
        length = str(len(message)).zfill(4)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServerEncrypted(self):
        length = self.socket.recv(4)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        message = self.sklib.OTPDecrypt(message,self.skkm.getSessionOTP())
        return message

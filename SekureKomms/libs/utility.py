class Utility:

    def __init__(self,socket,sklib,skkm):
        self.socket = socket
        self.sklib = sklib
        self.skkm = skkm
        self.lengthField = 5

    def sendToServer(self,message):
        # print("Sending",message)
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromClient(self):
        length = self.socket.recv(self.lengthField)
        if "GET " in length.decode():
            return "GET"
        length = int(length.decode())
        message = self.socket.recv(length)
        return message.decode()

    def sendToClient(self,message):
        # print("Sending",message)
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServer(self):
        length = self.socket.recv(self.lengthField)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        return message

    def sendToServerEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.skkm.getSessionOTP())
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromClientEncrypted(self):
        length = self.socket.recv(self.lengthField)
        # print(length)
        length = int(length.decode())
        message = self.socket.recv(length)
        message = message.decode()
        message = self.sklib.OTPDecrypt(message,self.skkm.getSessionOTP())
        return message

    def sendToClientEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.skkm.getSessionOTP())
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        self.socket.send(message.encode())

    def recvFromServerEncrypted(self):
        length = self.socket.recv(self.lengthField)
        length = int(length.decode())
        message = self.socket.recv(length).decode()
        message = self.sklib.OTPDecrypt(message,self.skkm.getSessionOTP())
        return message

    def clientNegotiateSecurity(self):
        self.sendToServer('negotiateSecurity'+self.sklib.getToken())
        self.sendToServer(self.skkm.exportRSAKey())
        self.skkm.importRemoteRSAPublic(self.recvFromServer())
        self.skkm.setSessionOTP(self.sklib.generateOTPKey())
        self.sendToServer(self.sklib.RSAEncrypt(self.skkm.getSessionOTP(),self.skkm.getRemotePublic()))
        if self.skkm.getRemotePublic() and self.skkm.getSessionOTP():
            print("Communication security negotiated...")
            input("Press enter to continue...")
        else:
            # print("getRemotePublic",self.skkm.getRemotePublic())
            # print("getSessionOTP",self.skkm.getSessionOTP())
            print("Exception raised in negotiateSecurity, press enter to continue...")
            raise Exception('NegotiateSecurityException')

    def serverNegotiateSecurity(self):
        self.skkm.importRemoteRSAPublic(self.recvFromClient())
        self.sendToClient(self.skkm.exportRSAKey())
        self.skkm.setSessionOTP(self.sklib.RSADecrypt(self.recvFromClient(),self.skkm.getPrivateKey()))
        if self.skkm.getRemotePublic() and self.skkm.getSessionOTP():
            print("Security negotiated with client")
            self.mode = 'secure'
        else:
            raise Exception('NegotiateSecurityException')

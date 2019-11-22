import json

class Utility:

    def __init__(self,socket,sklib,skkm):
        self.socket = socket
        self.sklib = sklib
        self.skkm = skkm
        self.lengthField = 8
        self.maxpayloadsize = 128

    def setSocket(self,socket):
        self.socket = socket

    def sendToServer(self,message):
        length = str(len(message)).zfill(self.lengthField)
        # print("Send len:%s message len: %s"%(length,len(message)))
        self.socket.send(length.encode())
        bytecount = 0
        if len(message) < self.maxpayloadsize:
            self.socket.send(message.encode())
        else:
            while bytecount < len(message):
                tempmessage = message[bytecount:bytecount+self.maxpayloadsize]
                self.socket.send(tempmessage.encode())
                bytecount += len(tempmessage)

    def recvFromClient(self):
        length = self.socket.recv(self.lengthField)
        if "GET " in length.decode():
            return "GET"
        else:
            length = int(length.decode())
        message = ""
        bytecount = 0
        if length < self.maxpayloadsize:
            message = self.socket.recv(length)
        else:
            while bytecount < length:
                if (length-bytecount) >= self.maxpayloadsize:
                    tempmessage = self.socket.recv(self.maxpayloadsize)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
                else:
                    tempmessage = self.socket.recv(length-bytecount)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
        return message

    def sendToClient(self,message):
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        bytecount = 0
        if len(message) < self.maxpayloadsize:
            self.socket.send(message.encode())
        else:
            while bytecount < len(message):
                tempmessage = message[bytecount:bytecount+self.maxpayloadsize]
                self.socket.send(tempmessage.encode())
                bytecount += self.maxpayloadsize

    def recvFromServer(self):
        length = self.socket.recv(self.lengthField)
        length = int(length.decode())
        message = ""
        bytecount = 0
        if length < self.maxpayloadsize:
            message = self.socket.recv(length)
        else:
            while bytecount < length:
                if (length-bytecount) >= self.maxpayloadsize:
                    tempmessage = self.socket.recv(self.maxpayloadsize)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
                else:
                    tempmessage = self.socket.recv(length-bytecount)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
        return message

    def sendEncrypted(self,message):
        message = self.sklib.OTPEncrypt(message,self.skkm.getSessionOTP())
        length = str(len(message)).zfill(self.lengthField)
        self.socket.send(length.encode())
        bytecount = 0
        if len(message) < self.maxpayloadsize:
            self.socket.send(message.encode())
        else:
            while bytecount < len(message):
                tempmessage = message[bytecount:bytecount+self.maxpayloadsize]
                self.socket.send(tempmessage.encode())
                bytecount += self.maxpayloadsize

    def recvEncrypted(self):
        length = self.socket.recv(self.lengthField)
        length = int(length.decode())
        message = ""
        bytecount = 0
        if length < self.maxpayloadsize:
            message = self.socket.recv(length)
            message = message.decode()
        else:
            while bytecount < length:
                if (length-bytecount) >= self.maxpayloadsize:
                    tempmessage = self.socket.recv(self.maxpayloadsize)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
                else:
                    tempmessage = self.socket.recv(length-bytecount)
                    message += tempmessage.decode()
                    bytecount += len(tempmessage)
        message = self.sklib.OTPDecrypt(message,self.skkm.getSessionOTP())
        return message


    def clientNegotiateSecurity(self):
        self.sendToServer('negotiateSecurity'+self.sklib.getToken())
        self.sendToServer(self.skkm.exportRSAKey())
        self.skkm.importRemoteRSAPublic(self.recvFromServer())
        self.skkm.setSessionOTP(self.sklib.generateOTPKey())
        sessionOTP = json.dumps(self.skkm.getSessionOTP())
        self.sendToServer(self.sklib.RSAEncrypt(sessionOTP,self.skkm.getRemotePublic()))
        if self.skkm.getRemotePublic() and self.skkm.getSessionOTP():
            print("Communication security negotiated...")
        else:
            input("Exception raised in negotiateSecurity, press enter to continue...")
            raise Exception('NegotiateSecurityException')

    def serverNegotiateSecurity(self):
        data = self.recvFromClient()
        if data == 'negotiateSecurity'+self.sklib.getToken():
            self.skkm.importRemoteRSAPublic(self.recvFromClient())
            self.sendToClient(self.skkm.exportRSAKey())
            sessionOTP = self.sklib.RSADecrypt(self.recvFromClient(),self.skkm.getPrivateKey())
            sessionOTP = json.loads(sessionOTP)
            self.skkm.setSessionOTP(sessionOTP)
            if self.skkm.getRemotePublic() and self.skkm.getSessionOTP():
                print("Security negotiated with client")
            else:
                raise Exception('NegotiateSecurityException')
        else:
            pass

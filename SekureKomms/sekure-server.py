import socket

class SekureServer:

    def __init__(self):
        self.__startServer()

    def __startServer(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(("127.0.0.1",4444))
        self.s.listen(1)
        conn, addr = self.s.accept()
        self.s.close()

    def run(self):
        pass

ss = SekureServer()

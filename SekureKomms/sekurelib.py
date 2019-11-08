from Crypto.Hash import SHAKE256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from binascii import hexlify
import uuid

class SekureLib:
    def __init__(self):
        self.rounds = 10000

    def generateRSAKeyPair(self):
        private = RSA.generate(2048)
        public = private.publickey()
        return [private,public]

    def RSAEncrypt(self,message,publickey):
        cipher_rsa = PKCS1_OAEP.new(publickey)
        return cipher_rsa.encrypt(message.encode()).hex()

    def RSADecrypt(self,message,privatekey):
        message = bytearray.fromhex(message)
        cipher_rsa = PKCS1_OAEP.new(privatekey)
        return cipher_rsa.decrypt(message).decode()

    def AESEncrypt(self,message,key):
        key = bytearray(key,'utf8')
        key = pad(key,AES.block_size)
        message = bytearray(message,'utf8')
        cipher_aes = AES.new(key,AES.MODE_CBC)
        ct_bytes = pad(message,AES.block_size)
        ct_bytes = cipher_aes.encrypt(ct_bytes)
        return "%s:%s"%(cipher_aes.iv.hex(),ct_bytes.hex())

    def AESDecrypt(self,message,key):
        key = bytearray(key,'utf8')
        key = pad(key,AES.block_size)
        iv,ct = message.split(':')
        iv = bytearray.fromhex(iv)
        ct = bytearray.fromhex(ct)
        cipher_aes = AES.new(key,AES.MODE_CBC,iv)
        pt_bytes = cipher_aes.decrypt(ct)
        pt = unpad(pt_bytes,AES.block_size).decode()
        return pt

    def generateAESKey(self,privatekey):
        keybytes = get_random_bytes(16)
        cipher_rsa = PKCS1_OAEP.new(privatekey)
        aeskey = cipher_rsa.encrypt(keybytes)
        return aeskey.hex()

    def generateHMACSecret(self):
        keybytes = get_random_bytes(16)
        shake = SHAKE256.new()
        shake.update(keybytes)
        out = hexlify(shake.read(32))
        for count in range(self.rounds):
            shake = SHAKE256.new()
            shake.update(out)
            out = hexlify(shake.read(32))
        return out.decode()

    def generateUUID(self):
        id = uuid.uuid4()
        return id

    def generateOTPKey(self,password):
        shake = SHAKE256.new()
        shake.update(password.encode())
        out = hexlify(shake.read(4096))
        for count in range(self.rounds):
            shake = SHAKE256.new()
            shake.update(out)
            out = hexlify(shake.read(4096))
        return out

    def OTPEncrypt(self,ptmessage,key):
        ctmessage=bytearray('','utf8')
        if len(key) < len(ptmessage):
            print("Keysize is too small")
            return None
        if type(key) == str:
            key = key.encode()
        if type(ptmessage) == str:
            ptmessage = ptmessage.encode()
        for index in range(len(ptmessage)):
            ctmessage.append(ptmessage[index]^key[index])
        return ctmessage.hex()

    def OTPDecrypt(self,ctmessage,key):
        ptmessage = bytearray('','utf8')
        ctmessage = bytearray.fromhex(ctmessage)
        if len(key) < len(ctmessage):
            print("Keysize is too small")
            return None
        if type(key) == str:
            key = key.encode()
        for index in range(len(ctmessage)):
            ptmessage.append(ctmessage[index]^key[index])
        return ptmessage.decode()

    def __struck(self):
        print("just for fun")

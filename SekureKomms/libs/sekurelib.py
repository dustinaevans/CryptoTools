from Crypto.Hash import SHAKE256
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA512
from binascii import hexlify
import uuid

class SekureLib:
    def __init__(self):
        pass
    def generateSHA(self,data):
        hash_obj = SHA512.new()
        hash_obj.update(bytes(data,'utf8'))
        return hash_obj.hexdigest()

    def generateRSAKeyPair(self):
        private = RSA.generate(2048)
        public = private.publickey()
        return [private,public]

    def RSAEncrypt(self,message,publickey):
        rsaStandardSize = 245
        cipher_rsa = PKCS1_OAEP.new(publickey)
        message = bytearray(message,'utf8')
        temparray = bytearray('','utf8')
        ciphertext = ""
        for char in message:
            templength = len(temparray)
            if (templength < rsaStandardSize):
                temparray.append(char)
            if (templength == rsaStandardSize):
                ciphertext.append(cipher_rsa.encrypt(temparray).hex())
                temparray = bytearray('','utf8')
        return ciphertext

    def RSADecrypt(self,message,privatekey):
        rsaStandardSize = 245
        message = bytearray.fromhex(message)
        temparray = bytearray('','utf8')
        plaintext =  ""
        cipher_rsa = PKCS1_OAEP.new(privatekey)
        for char in message:
            templength = len(temparray)
            if (templength < rsaStandardSize):
                temparray.append(char)
            if (templength == rsaStandardSize):
                plaintext.append(cipher_rsa.decrypt(temparray).decode())
                temparray = bytearray('','utf8')
        return plaintext

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

    def generateAESKey(self,publickey):
        keybytes = get_random_bytes(16).hex()
        aeskey = self.generateSHA(keybytes)
        for i in range(10000):
            aeskey = self.generateSHA(aeskey)
        return aeskey

    def generateHMACSecret(self):
        keybytes = get_random_bytes(16)
        shake = SHAKE256.new()
        shake.update(keybytes)
        out = hexlify(shake.read(32))
        for count in range(10000):
            shake = SHAKE256.new()
            shake.update(out)
            out = hexlify(shake.read(32))
        return out.decode()

    def generateUUID(self):
        id = uuid.uuid4()
        return str(id)

    def generateOTPKey(self):
        shake = SHAKE256.new()
        shake.update(get_random_bytes(16))
        out = hexlify(shake.read(4608))
        for count in range(10000):
            shake = SHAKE256.new()
            shake.update(out)
            shake.update(get_random_bytes(16))
            out = hexlify(shake.read(4608))
        return out.decode()

    def OTPEncrypt(self,ptmessage,key):
        ctmessage=bytearray('','utf8')
        if len(key) < len(ptmessage):
            print("Encrypt Keysize is too small")
            print(len(key)," Compared to ",len(ptmessage))
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
            print("Decrypt Keysize is too small")
            print(len(key)," Compared to ",len(ctmessage))
            return None
        if type(key) == str:
            key = key.encode()
        for index in range(len(ctmessage)):
            ptmessage.append(ctmessage[index]^key[index])
        return ptmessage.decode()

    def __struck(self):
        print("just for fun")

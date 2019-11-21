from Crypto.Hash import SHAKE256,MD5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA512
from binascii import hexlify
import uuid, time

class SekureLib:
    def __init__(self):
        self.debug = False
        self.token = "1234509876"

    def generateSHA(self,data):
        hash_obj = SHA512.new()
        hash_obj.update(bytes(data,'utf8'))
        return hash_obj.hexdigest()

    def generateMD5(self,data):
        hash_obj = MD5.new()
        hash_obj.update(data.encode())
        return hash_obj.hexdigest()

    def generateRSAKeyPair(self):
        self.logshit("sekurelib.generateRSAKeyPair")
        private = RSA.generate(2048)
        public = private.publickey()
        return [private,public]

    def RSAEncrypt(self,message,publickey):
        self.logshit("sekurelib.RSAEncrypt")
        rsaStandardSize = 200
        cipher_rsa = PKCS1_OAEP.new(publickey)
        temparray = ""
        ciphertext = ""
        count = 0
        for i in range(len(message)):
            if count < rsaStandardSize:
                temparray += message[i]
                count += 1
            if (count == rsaStandardSize) or (i == len(message)-1):
                temp = cipher_rsa.encrypt(temparray.encode())
                temp = temp.hex()
                ciphertext += temp
                temparray = ""
                count = 0
        return ciphertext

    def RSADecrypt(self,message,privatekey):
        self.logshit("sekurelib.RSADecrypt")
        rsaStandardSize = 512
        cipher_rsa = PKCS1_OAEP.new(privatekey)
        temparray = ""
        plaintext =  ""
        count = 0
        for i in range(len(message)):
            if count < rsaStandardSize:
                temparray += message[i]
                count += 1
            if (count == rsaStandardSize) or (i == len(message)):
                temp = cipher_rsa.decrypt(bytearray.fromhex(temparray))
                temp = temp.decode()
                temparray = ""
                plaintext += temp
                count = 0
        return plaintext

    def AESEncrypt(self,message,key):
        self.logshit("sekurelib.AESEncrypt")
        key = bytearray(key,'utf8')
        key = pad(key,AES.block_size)
        message = bytearray(message,'utf8')
        cipher_aes = AES.new(key,AES.MODE_CBC)
        ct_bytes = pad(message,AES.block_size)
        ct_bytes = cipher_aes.encrypt(ct_bytes)
        return "%s:%s"%(cipher_aes.iv.hex(),ct_bytes.hex())

    def AESDecrypt(self,message,key):
        self.logshit("sekurelib.AESDecrypt")
        key = bytearray(key,'utf8')
        key = pad(key,AES.block_size)
        iv,ct = message.split(':')
        iv = bytearray.fromhex(iv)
        ct = bytearray.fromhex(ct)
        cipher_aes = AES.new(key,AES.MODE_CBC,iv)
        pt_bytes = cipher_aes.decrypt(ct)
        pt = unpad(pt_bytes,AES.block_size).decode()
        return pt

    def generateAESKey(self):
        self.logshit("sekurelib.generateAESKey")
        keybytes = get_random_bytes(16).hex()
        aeskey = self.generateSHA(keybytes)
        for i in range(10000):
            aeskey = self.generateSHA(aeskey)
        return aeskey[:16]

    def generateHMACSecret(self):
        self.logshit("sekurelib.generateHMACSecret")
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
        self.logshit("sekurelib.generateUUID")
        id = uuid.uuid4()
        return str(id)

    def generateOTPKey(self):
        self.logshit("sekurelib.generateOTPKey")
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
        self.logshit("sekurelib.OTPEncrypt")
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
        self.logshit("sekurelib.OTPDecrypt")
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

    def getToken(self):
        token = self.generateSHA(self.token)
        return token

    def logshit(self,message):
        if self.debug:
            print(message)

    def __struck(self):
        self.logshit("dunderstruck")

    def testSelf(self):
        failures = 0
        print("Testing sekurelib internals")
        sha = self.generateSHA("abcde")
        if sha.upper() == "878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1":
            print("SHA: [OK]")
        else:
            failures += 1
            print("SHA: [FAIL]")
        keypair = self.generateRSAKeyPair()
        if len(keypair) == 2:
            print("RSA KEYPAIR: [OK]")
        else:
            failures += 1
            print("RSA KEYPAIR: [FAIL]")
        encrypt = self.RSAEncrypt("878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1",keypair[1])
        decrypt = self.RSADecrypt(encrypt,keypair[0])
        if decrypt == '878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1878AE65A92E86CAC011A570D4C30A7EAEC442B85CE8ECA0C2952B5E3CC0628C2E79D889AD4D5C7C626986D452DD86374B6FFAA7CD8B67665BEF2289A5C70B0A1':
            print("RSA Module: [OK]")
        else:
            failures += 1
            print("RSA Module: [FAIL]")
        aeskey = self.generateAESKey()
        if aeskey:
            print("AES Keygen: [OK]")
        else:
            failures += 1
            print("AES Keygen: [FAIL]")
        encrypt = self.AESEncrypt("abcde",aeskey)
        decrypt = self.AESDecrypt(encrypt,aeskey)
        if decrypt == "abcde":
            print("AES Module: [OK]")
        else:
            failures += 1
            print("AES Module: [FAIL]")
        uuid = self.generateUUID()
        if uuid:
            print("UUID Module: [OK]")
        else:
            failures += 1
            print("UUID Module: [FAIL]")
        otp = self.generateOTPKey()
        if len(otp) > 0:
            print("OTP Generate: [OK]")
        else:
            failures += 1
            print("OTP Generate: [FAIL]")
        encrypt = self.OTPEncrypt("abcde",otp)
        decrypt = self.OTPDecrypt(encrypt,otp)
        if decrypt == "abcde":
            print("OTP Module: [OK]")
        else:
            failures += 1
            print("OTP Module: [FAIL]")
        if failures > 0:
            print("%s modules failed."%failures)
            input("Press enter to quit...")
            exit(-1)
        else:
            print("All modules passed testing.")
            time.sleep(2)

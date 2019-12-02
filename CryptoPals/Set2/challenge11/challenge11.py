from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes as randBytes
from Crypto.Util import strxor
from base64 import b64decode
import random

def pad(data,length):
    if len(data)%length == 0:
        if type(data) == str:
            return data.encode()
        else:
            return data
    else:
        padlen = (length-(len(data)%length))
        if type(data) != str:
            padval = chr(padlen).encode()
        else:
            padval = chr(padlen)
        padding = padval*padlen
        data = data+padding
        return data.encode()

def unpad(data,length):
    lastblock = data[len(data)-16:len(data)]
    paddingChar = lastblock[-1]
    padcount = lastblock.count(paddingChar)
    if padcount == paddingChar:
        for i in range(padcount):
            data.pop(-1)
    return data

def xor(string1,string2):
    xorz = bytearray()
    for i in range(len(string1)):
        xorz.append(string1[i]^string2[i])
    return xorz

def ECBEncrypt(string1,key):
    cipher = AES.new(key, AES.MODE_ECB)
    string1 = pad(string1,16)
    return cipher.encrypt(string1)

def CBCEncrypt(iv,data,key):
    cipherlength = 16
    cipher = AES.new(key, AES.MODE_ECB)
    ct = bytearray()
    numblocks = 0
    if len(data)%cipherlength != 0:
        numblocks = (len(data)//cipherlength)+1
    else:
        numblocks = (len(data)//cipherlength)
    # print("Num encryption block: %s"%numblocks)
    iv = pad(iv,cipherlength)
    previousBlock = iv
    for i in range(numblocks):
        currentPTBlock = bytearray(data[i*cipherlength:(i*cipherlength)+cipherlength])
        currentPTBlock = pad(currentPTBlock,cipherlength)
        intermediateBlock = xor(currentPTBlock,previousBlock)
        previousBlock = cipher.encrypt(intermediateBlock)
        ct += previousBlock
    ct += previousBlock
    return ct

def CBCDecrypt(data,key,iv=None):
    cipherlength = 16
    if not iv:
        iv = data[:cipherlength]
    cipher = AES.new(key, AES.MODE_ECB)
    pt = bytearray()
    previousBlock = iv
    data = data[cipherlength:]
    numblocks = len(data)//cipherlength
    for i in range(numblocks):
        currentCTBlock = bytearray(data[i*cipherlength:(i*cipherlength)+cipherlength])
        intermediateBlock = cipher.decrypt(currentCTBlock)
        currentPTBlock = xor(intermediateBlock,previousBlock)
        pt += currentPTBlock
        previousBlock = currentCTBlock
    return unpad(pt,cipherlength)

def encryptionOracle(input):
    iv = randBytes(16)
    randkey = randBytes(16)
    precount = random.randrange(5,10)
    postcount = random.randrange(5,10)
    mode = random.randrange(2)
    pre = randBytes(precount).hex()[:5]
    post = randBytes(postcount).hex()[:5]
    pt = pre+input+post
    if mode == 0:
        print("CBC")
        # print("Input: %s"%input)
        # print("randkey: %s"%randkey)
        # print("precount: %s"%precount)
        # print("postcount: %s"%postcount)
        # print("pre: %s"%pre)
        # print("post: %s"%post)
        # print("PT: %s"%pt)
        ct = CBCEncrypt(pt,randkey,iv)
        return ct
    else:
        print("ECB")
        ct = ECBEncrypt(pt,randkey)
        return ct

def getOracle(input):
    oracle = encryptionOracle("asdfasdfasdf")
    while True:
        if len(oracle) == 32:
            print(oracle[10:][:10])
            break
        oracle = encryptionOracle("asdfasdfasdf")

def getDifferential():
    test1 = "asdf"
    test2 = "a"
    oracle = encryptionOracle(test1+test2)
    if len(oracle) == 16:
        print('Mode: ECB')
    elif len(oracle) == 32:
        print('Mode: CBC')
    else:
        print('Mode: Unk')


getDifferential()

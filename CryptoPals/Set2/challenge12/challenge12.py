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
        if type(data) == str:
            return data.encode()
        else:
            return data

def unpad(data,length):
    lastblock = data[len(data)-16:len(data)]
    paddingChar = lastblock[-1]
    padcount = lastblock.count(paddingChar)
    if padcount == paddingChar:
        for i in range(padcount):
            data.pop(-1)
    return data

def ECBEncrypt(string1,key):
    cipher = AES.new(key, AES.MODE_ECB)
    string1 = pad(string1,AES.block_size)
    return cipher.encrypt(string1)


def makeUnkString(input,blocknum):
    randkey = b"_\xc0\x8c\xa4,??\x05\xed\xf9\xe9\xb7%\xaaW\xc9"
    addedstr = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    addedstr = b64decode(addedstr)
    pt = input
    pt = pt+addedstr
    ct = ECBEncrypt(pt,randkey)
    start = 16*blocknum
    end = 16*(blocknum+1)
    return ct[start:end]

# Rollin' in my 5.0\nWith my rag-top down so my hair
pt = ""
for blocknum in range(10):
    testbytes="AAAAAAAAAAAAAAA"
    for count in range(15,-1,-1):
        startval = makeUnkString(bytes(testbytes[:count],'utf8'),blocknum)
        for i in range(255):
            key = testbytes[:count]+pt+chr(i)
            testval = makeUnkString(bytes(key,'utf8'),blocknum)
            if testval == startval:
                # print(chr(i),count,pt,key)
                pt += chr(i)
                break
print(pt)
# pt = ""
# for blocknum in range(16):
#     padstr = ""
#     startval = makeUnkString(bytes(padstr,'utf8'),blocknum)
#     for i in range(255):
#         key = pt+chr(i)
#         padcount = 16-len(key)%16
#         # print(padcount)
#         padstr = "A"*padcount
#         testbytes = bytes(padstr+key,'utf8')
#         testval = makeUnkString(testbytes,blocknum)
#         if testval == startval:
#             pt += chr(i)
#             print("Hit:",)
# print(pt)

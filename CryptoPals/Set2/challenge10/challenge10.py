from Crypto.Cipher import AES
from base64 import b64decode

def pad(data,length):
    if len(data)%length == 0:
        return data
    else:
        padlen = (length-(len(data)%length))
        padval = chr(padlen).encode()
        print(padlen,padval)
        padding = padval*padlen
        return data+padding

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
        ct += previousBlock
        previousBlock = cipher.encrypt(intermediateBlock)
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


key = b"YELLOW SUBMARINE"
iv = b"\x00\x00\x00 &c"
iv = pad(iv,16)

fd = open('10.txt','rb')
ct = fd.read()
ct = b64decode(ct)
pt = CBCDecrypt(ct,key)
print(pt.decode())
# cipher = AES.new(key, AES.MODE_ECB)
# pt = cipher.decrypt(ct).decode()
# print(pt)

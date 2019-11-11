def b64DecodeFile(filename):
    from base64 import b64decode
    fd = open(filename,'rb')
    b64 = fd.read()
    b64d = b64decode(b64)
    return b64d

def getTwoPieces(keysize,data):
    tempdata = bytearray('','utf8')
    retval = [[],[]]
    for count in range(keysize):
        retval[0].append(data[count])
        retval[1].append(data[count+10])
    return retval

def computeHammingDistance(string1,string2,keysize):
    from bitstring import BitArray
    if type(string1)==str:
        string1 = bytearray(string1,'utf8')
        string2 = bytearray(string2,'utf8')
    total = 0
    for count in range(len(string1)):
        byte1 = BitArray(int=string1[count],length=8)
        byte2 = BitArray(int=string2[count],length=8)
        for bit in range(len(byte1)):
            if byte1[bit] == byte2[bit]:
                pass
            else:
                total+=1
    return total/keysize

def determineKeySize(data,minkeysize,maxkeysize):
    results = []
    for size in range(minkeysize,maxkeysize):
        pieces = getTwoPieces(size,data)
        distance = computeHammingDistance(pieces[0],pieces[1],size)
        results.append([size,distance])
    retval = None
    for result in results:
        if not retval:
            retval = result
        elif result[1] < retval[1]:
            retval = result
        else:
            pass
    return retval[0]

def calculateIC(textbytes):
    result = None
    try:
        text=""
        if type(textbytes) == bytes:
            text = textbytes.decode().lower()
        elif type(textbytes) == str:
            text = textbytes.lower()
        elif type(textbytes) == bytearray:
            text = textbytes.decode().lower()
        else:
            pass
        textlength = 0
        result = []
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for letter in letters:
            temp = {'letter':letter,'count':0}
            for char in text:
                if char == letter:
                    temp['count'] += 1.00
            result.append(temp)
        ic = 0
        for thing in result:
            count = thing['count']
            ic += count*(count-1.00)
        return ic/(textlength*(textlength-1.00))
    except Exception as e:
        print(e)
        return 2.5

def getBlocks(textbytes,keysize):
    if type(textbytes) == str:
        textbytes = bytearray(textbytes,'utf8')
    keysize = keysize
    array1 = []
    counter = 0
    temparray = []
    for char in textbytes:
        if (counter%(keysize) == 0) and (counter != 0):
            array1.append(temparray)
            temparray = []
        temparray.append(char)
        counter+=1
    return array1

def transposeBlocks(blocks):
    import numpy as np
    transposed = np.transpose(blocks)
    return transposed.tolist()

def xorDecrypt(sourcehex,key):
    if type(sourcehex) == str:
        sourcehex = bytearray.fromhex(sourcehex)
    dest = bytearray.fromhex('') # just makes an empty bytearray
    for b in sourcehex:
        dest.append(b^key)
    try:
        dest = dest.decode()
    except:
        pass
    return dest

data = b64DecodeFile('./6.txt')
keysize = determineKeySize(data,2,40)
print("Keysize: %s"%keysize)
blocks = getBlocks(data,keysize)
print("Total blocks: %s"%len(blocks))
print("Expected blocks: %s"%(len(data)//keysize))
print("Length of each block: %s"%len(blocks[0]))
print("TextLength: %s"%len(data))
print("Text length / keysize: %s"%(len(data)/keysize))
transposed = transposeBlocks(blocks)
xorResults = []
selectedResults = []
for block in transposed:
    for char in range(255):
        xor = xorDecrypt(block,char)
        ic = calculateIC(xor)
        xorResults.append({'pt':xor,'score':ic})
    tempResult = {'pt':'','score':2}
    for result in xorResults:
        print(result)
        if result['score'] < tempResult['score']:
            tempResult = result
    selectedResults.append(tempResult)
    break

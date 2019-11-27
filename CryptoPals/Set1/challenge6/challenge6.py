def b64DecodeFile(filename):
    from base64 import b64decode
    fd = open(filename,'rb')
    b64 = fd.read()
    b64d = b64decode(b64)
    return b64d

def getTwoPieces(keysize,data):
    tempdata = bytearray('','utf8')
    piece1 = data[:keysize]
    piece2 = data[keysize:(keysize*2)]
    return [piece1,piece2]

def computeHammingDistance(string1,string2,keysize):
    return(sum(bin(byte).count('1') for byte in bytearray(string1[i]^string2[i] for i in range(len(string1)))))

def determineKeySize(data,minkeysize,maxkeysize):
    results = []
    for size in range(minkeysize,maxkeysize):
        score = 0
        count = 0
        while count < len(data):
            piece1 = data[count:size+count]
            piece2 = data[size+count:size+count*2]
        # pieces = getTwoPieces(size,data)
            score += computeHammingDistance(piece1,piece2,size)
        score /= (len(data)/size)
        results.append([size,distance])
    retval = None
    for result in results:
        print(result)
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
        # textbytes.replace(r"\\x[0-9][0-9]","").replace("\n","").replace("\r","")
        # print("textbytes",textbytes)
        textlength = len(textbytes)
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

def scoreBlock(textbytes):
    try:
        textbytes = textbytes.decode()
        textbytes = textbytes.lower()
    except:
        pass

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
    key = ord(key)
    if type(sourcehex) == str:
        sourcehex = bytearray.fromhex(sourcehex)
    dest = bytearray() # just makes an empty bytearray
    for b in sourcehex:
        dest.append(b^key)
    return dest

goodchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklnmopqrstuvwxyz1234567890"
data = b64DecodeFile('./6.txt')
keysize = determineKeySize(data,2,40)
print('keysize',keysize)
blocks = getBlocks(data,keysize)
transposed = transposeBlocks(blocks)
xorResults = []
selectedResults = []
for block in transposed:
    block = bytearray(block)
    for char in goodchars:
        xor = xorDecrypt(block,char)
        xorResults.append({'pt':xor,'score':calculateIC(xor),'key':char})
    tempResult = {'pt':'','score':10}
    for result in xorResults:
        # print(result)
        if result['score'] < tempResult['score']:
            tempResult = result
            selectedResults.append(tempResult)
for i in selectedResults:
    # print(i)
    pass
# print(selectedResults)


# newkey = "AF12"
# newkey = bytearray(newkey,'utf8')
# finalArray = []
# count = 0
# while count < len(data):
#     finalArray.append(data[count]^newkey[count%4])
#     count+=1
# finalstring = ""
# for char in finalArray:
#     finalstring += chr(char)
# print(finalstring)

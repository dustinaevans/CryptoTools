def b64DecodeFile(filename):
    from base64 import b64decode
    fd = open(filename,'r')
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
    return retval

def calculateIC(textbytes):
    result = None
    try:
        text=""
        if type(textbytes) == bytes:
            text = textbytes.decode().lower()
        elif type(textbytes) == str:
            text = textbytes.lower()
        else:
            print("paramater is not of type str or bytes")
            exit(1)
        textlength = 0
        result = []
        letters = 'abcdefghijklmnopqrstuvwxyz'
        for letter in text:
            if letter in letters:
                textlength += 1.00
        for letter in letters:
            temp = {'letter':letter,'count':0}
            for char in text:
                if char == letter:
                    temp['count'] += 1.00
            result.append(temp)
        ic = 0
        for thing in result:
            print(thing)
            count = thing['count']
            ic += count*(count-1.00)
        return ic/(textlength*(textlength-1.00))
    except:
        return None

def transposeBlocks(textbytes,keysize):
    if type(textbytes) == str:
        textbytes = bytearray(textbytes,'utf8')
    array1 = [[0]*keysize]*keysize
    counter = 0
    for char in textbytes:
        array1[]
        counter+=1

keysize = 10
file = b64DecodeFile('./6.txt')
determinedSize = determineKeySize(file,2,40)
print(determinedSize)
print(calculateIC(""))
transposeBlocks(file,determinedSize[0])

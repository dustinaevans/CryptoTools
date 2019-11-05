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

keysize = 10
file = b64DecodeFile('./6.txt')
determinedSize = determineKeySize(file,2,40)
print(determinedSize)

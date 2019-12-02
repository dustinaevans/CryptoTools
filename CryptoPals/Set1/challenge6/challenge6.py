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
        setcount = 0
        count = 0
        while count < len(data):
            piece1 = data[count:size+count]
            piece2 = data[size+count:size*2+count]
            # print(count,size,piece1,piece2)
            try:
                score += computeHammingDistance(piece1,piece2,size)
            except:
                pass
            count+=size
            setcount += 1
        results.append([size,score])
    retval = None
    for result in results:
        if not retval:
            retval = result
        elif result[1] < retval[1]:
            retval = result
        else:
            pass
    return retval[0]

def getBlocks(textbytes,keysize):
    blocks = [[0]]*keysize
    for i in range(len(blocks)):
        blocks[i] = bytearray(textbytes[i::keysize])
    return blocks

def xorDecrypt(sourcehex,key):
    key = ord(key)
    if type(sourcehex) == str:
        sourcehex = bytearray.fromhex(sourcehex)
    dest = bytearray() # just makes an empty bytearray
    for b in sourcehex:
        dest.append(b^key)
    return dest

def scoreDecryptedBlock(block):
    ascii_text_chars = list(range(97, 122)) + [32]
    return sum([ x in ascii_text_chars for x in block])

goodchars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklnmopqrstuvwxyz1234567890 :"
data = b64DecodeFile('./6.txt')
keysize = determineKeySize(data,2,40)
print('keysize',keysize)
blocks = getBlocks(data,keysize)
selectedResults = []
for block in blocks:
    xorResults = []
    block = bytearray(block)
    for char in goodchars:
        xor = xorDecrypt(block,char)
        xorResults.append({'pt':xor,'score':scoreDecryptedBlock(xor),'key':char})
    tempResult = {'pt':'','score':0}
    for result in xorResults:
        if result['score'] > tempResult['score']:
            tempResult = result
    selectedResults.append(tempResult)
key = ""
for i in selectedResults:
    key += i['key']
print(key)
key = bytearray(key,'utf8')
decryptedFile = ""
count = 0
for i in range(len(data)):
    decryptedFile += chr(data[i]^key[i%len(key)])
print(decryptedFile)









# def calculateIC(textbytes):
#     result = None
#     try:
#         text=""
#         if type(textbytes) == bytes:
#             text = textbytes.decode().lower()
#         elif type(textbytes) == str:
#             text = textbytes.lower()
#         elif type(textbytes) == bytearray:
#             text = textbytes.decode().lower()
#         else:
#             pass
#         # textbytes.replace(r"\\x[0-9][0-9]","").replace("\n","").replace("\r","")
#         # print("textbytes",textbytes)
#         textlength = len(textbytes)
#         result = []
#         letters = 'abcdefghijklmnopqrstuvwxyz'
#         for letter in letters:
#             temp = {'letter':letter,'count':0}
#             for char in text:
#                 if char == letter:
#                     temp['count'] += 1.00
#             result.append(temp)
#         ic = 0
#         for thing in result:
#             count = thing['count']
#             ic += count*(count-1.00)
#         return ic/(textlength*(textlength-1.00))
#     except Exception as e:
#         print(e)
#         return 2.5

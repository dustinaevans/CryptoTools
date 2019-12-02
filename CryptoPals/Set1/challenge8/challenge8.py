from Crypto.Cipher import AES
from base64 import b64decode

fd = open('8.txt','r')
linenumber = 1
for line in fd:
    line = line.strip()
    length = int(len(line)/32)
    blocks = []
    for i in range(length):
        blocks.append(line[i*32:(i*32)+32])
    for i in blocks:
        doublecount = 0
        for j in blocks:
            if i == j:
                doublecount+=1
        if doublecount > 1:
            print(linenumber,i,line)
            print(doublecount)
    linenumber += 1

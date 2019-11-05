key = "ICE"

string1 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

array1 = bytearray(string1,'utf8')

finalarray1 = bytearray('','utf8')

keyarray = bytearray(key,'utf8')

count = 0
while count < len(array1):
    finalarray1.append(array1[count]^keyarray[count%3])
    count += 1

print("Array1: %s"%finalarray1.hex())

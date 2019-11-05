
def computeHammingDistance(string1,string2):
    from bitstring import BitArray
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
    return(total)

keysize = 10
string1 = "this is a test"
string2 = "wokka wokka!!!"
print(computeHammingDistance(string1,string2))

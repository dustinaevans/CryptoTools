# Init 3 bytearrays and convert from hex
buffer1 = bytearray.fromhex('1c0111001f010100061a024b53535009181c')
buffer2 = bytearray.fromhex('686974207468652062756c6c277320657965')
buffer3 = bytearray.fromhex('')

# Iterate over the array using a counter
count = 0
# while the count is less than the length of buffer1 (36)
while count < len(buffer1):
    # XOR the count'th element of each array (order does not matter)
    # and append it to buffer3
    buffer3.append(buffer1[count]^buffer2[count])
    #increase count by one (++ is not available in python <sad face emoji> )
    count += 1

# interestingly, this print statement produces the output "bytearray(b"the kid don\'t play")"
# some additional code is required to get the desired result
print(buffer3)

# this produces the desired output by converting the bytes back into a hex string
print(buffer3.hex())

# just interested to see if the other two hex strings print and readable text
print(buffer1)
print(buffer2)

# buffer2 prints bytearray(b"hit the bull\'s eye")

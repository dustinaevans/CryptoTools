# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
This is where shit gets crazy. This could end up being a seriously long walkthrough and I'm not doing a TLDR;. With our new and improved scoring method, however, we should be able to pull this one off. Our challenge is to take a base64 encoded file, decode it and break the repeating key XOR that encrypted it. This is going to be challenging and I hope that I can help you understand what is going on with this one.

## Problem
First, it says, we have to make a function to compute the Hamming distance between two strings. This is nearly trivial because the Hamming distance is simply the number of bits that differ between the two strings. So first, we need to convert the strings to bytes and then we need to find a way to determine how many bits of those bytes are different. Note that when you compute the Hamming distance of two pieces of data, they need to contain the same number of bytes. So we are going to a loop like this `for count in range(len(bytearray)):`. This way, we can access the same position in each array at one time. We are also going to initialize a running total variable before the loop to keep track of how many bits are different. After some googling, I found out that we need to import the bitstring library so that we can convert the byte to a string of bits that we can count `from bitstring import BitArray`. Looks like we also need to install that package with pip, so I'll be including a requirements.txt. After some type adjustment and reading over the API for bitstring, I came up with a piece of code that does exactly what I explained and prints out the number 37, which is precisely what we needed. This will now become our hammingDistance function.

```python
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
```

So that was step 1. On to step 2. The site says that we need to take 2 portions of the ciphertext that are keysize in length (we haven't defined keysize yet) and compute the Hamming distance between them. We may end up having to a change our code because right now it only accepts strings. Let's start by choosing an arbitrary keysize, say... 10. `keysize=10` Now we need to make a function to base64 decode the file.

## Solution

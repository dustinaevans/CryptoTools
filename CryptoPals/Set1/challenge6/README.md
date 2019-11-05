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

```python
def b64DecodeFile(filename):
    from base64 import b64decode
    fd = open(filename,'r')
    b64 = fd.read()
    b64d = b64decode(b64)
    fd.close()
    return b64d
```

This function opens the file, reads in the data, base64 decodes it and returns the decoded data. The next step is to get two pieces of that data that are keysize bytes long. So lets make a function that returns an array with two elements that consist of the two pieces of data.

```python
def getTwoPieces(keysize,data):
    tempdata = bytearray('','utf8')
    retval = [[],[]]
    for count in range(keysize):
        retval[0].append(data[count])
        retval[1].append(data[count+10])
    return retval/keysize
```

The next step is to compute the Hamming distance between the two pieces. I will now have to modify our Hamming distance function because it only takes in strings and we are trying to give it bytes. I just added the following:

```python
if type(string1)==str:
      string1 = bytearray(string1,'utf8')
      string2 = bytearray(string2,'utf8')
```

If it is as string, cast to bytearray, else we assume that it is a bytearray already. I almost forgot, we have to normalize this value by dividing by the keysize. I added this to the return statement.

The next step is to determine the size of the key. So we will create a new function for this and it will utilize the other functions that we created.

```python
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
```

When we run this, we get a keysize of 9 with a normalized distance of 3.11... So now, we have our potential keysize. The website says to break the data into blocks of the keysize that we determined in the last step and perform some other operations on them. Also, the website says to use histograms and our scoring method did not use this technique. One thing we could do is look for invalid ASCII characters when bruteforcing each transposed block (I will explain the transposition process in a bit). This will, at least, give us a good idea of where the key is in the range of 0-255. Before we begin that process, let's talk about the transposition process. First, we grab keysize number of blocks that are keysize long. This gives us a nice mathematical square. Then, we loop over `for x in range(keysize)` and get the current x'th byte from each block and put those into an array. This will give us an array that is `[keysize][keysize]` large that contains bytes that are encrypted with the same key. Let's look at a visual representation of this with a keysize of 4.

```
data = ABCDEFGHIJKLMNOPQRSTUVWXYZ
blocks = [[ABCD],[EFGH],[IJKL],[MNOP]]
array = [[AEIM],[BFJN],[CGKO],[DHLP]]
```
After you have this array, you can treat each block as a single-byte XOR problem. However, you do not have the benefit of using quadgrams to determine the fitness of each block because, even if you do find the key for a block, the other 3 letters of the quadgram will be in the remaining 3 blocks. So, we will need one more tool to determine the fitness of each block and then we can determine the fitness of the overall string. The other tool we will be using is the index of coincidence. This tool will give you a good measure of how close the decrypted text is to English. I'm not going to go over the code because it took me a while to get it right and I don't entirely understand all of it. You can find more information at http://practicalcryptography.com/cryptanalysis/text-characterisation/index-coincidence/. Now We need to create the function that transposes our text.

## Solution

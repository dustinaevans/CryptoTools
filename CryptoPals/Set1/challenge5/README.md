# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
Encrypt two strings using repeating key XOR.

## Problem
This is similar to what we did in challenge 3 except instead of using one byte, we use 3. This is really simple because we just do the same thing but iterate over the key multiple times. It is likely that we will run into the problem where the plaintext size is not a multiple of the key size. For example, if we have a key of size 3 and a text of size 10, we would loop over the key 3 times and have one character left over. There are two ways to deal with this:
1. Padding the plaintext to make it a multiple of the keysize (which is what we see in AES)
2. Simply use part of the key on the remaining bytes. This is what we will be doing.

Padding, if not done correctly, can lead to a sort of plaintext attack. The attacker can guess that the last few bytes are padding and attempt to coerce a key from them. If our plaintext were 10 characters and we added a padding of two bytes but we padded with zero, the last two bytes of the ciphertext would be the key. If we padded with any other value but used the same one for both padding bytes, we would have repeating characters at the end and the attacker would know that this is padding. Similar to how base64 pads its strings.

```
blabla is YmxhYmxhCg==

blablab is YmxhYmxhYgo=

blablabl is YmxhYmxhYmwK
```

So you can see the padding at the end of the resulting ciphertext. This isn't always a problem but we really don't want to give the attacker anymore information than they already have.

## Solution
So lets talk about the algorithm that we are going to use. We are going to convert the strings and key to bytes using bytearray. Then we will use a counter to keep track of where we are and loop over the bytearrays. We use a counter so that we can take advantage of modulo operator to access each letter of the key. If we user key[counter%3], we will get I C E I C E and so on. We then use that value to XOR the bytearrays and print them at the end. I could probably be crafty and do this in one loop but for simplicity, I will use one for each plaintext string.

1. Convert the string to bytes using bytearray
2. Init a counter
3. Loop over the arrays
4. XOR array[counter] with key[counter%3]
5. Update counter
6. Print each array

```python
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

```


EDIT: There is only one string and it has a `\n` character in it

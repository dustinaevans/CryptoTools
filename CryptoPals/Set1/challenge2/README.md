# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
This challenge involves a fixed size XOR operation. XOR is known to the math world as addition modulo 2.
Excerpt from wolfram.com:
```
... This definition is quite common in computer science, where XOR is usually thought of as addition modulo 2. ...
http://mathworld.wolfram.com/XOR.html
```

## Problem
The problem is to create two buffers of the same length and XOR them to produce the required result.
```
1c0111001f010100061a024b53535009181c
XOR
686974207468652062756c6c277320657965
Produces
746865206b696420646f6e277420706c6179
```

## Solution
Again, we need to convert these to bytes. The obvious solution is to use the bytearray function from the last challenge and iterate over the two, XOR each pair and write that pair into a new bytearray. We can make one loop to perform all 3 operations.

# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
The challenge is to convert a string of hex to base64.

## Problem
The specific problem is that converting the string directly to base64 yields a different value than the one that is expected. This is because the base64 function can operate on many data types.

## Solution
Converting they hex string to bytes via bytearray.fromhex(), yields the correct result. This is mentioned in the hint on the website "Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.". This means that you should first convert the hex string to bytes and then perform the base64 encode function on those bytes.

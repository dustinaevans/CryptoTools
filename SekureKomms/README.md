# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
To create a secure communications program/algorithm

## Problem

## Solution


## Notes
Zero knowledge system (computer has zero knowledge of the private key)
PK Cryptography
Two factor keys on both sides
Symmetric keys exchanged via PK
HMAC keys exchanged at the same time
One time pad used to encrypt communications
OTP keys are used for one session and then purged
Key size starts at 32,768 bits or 4096 characters
MessageID is SHA-512 hash of the key GUID

```
Encrypted message format:
messageID(plaintext).<encrypted message>.length.<SHA-512 HMAC>

```

```
Decrypted message format:

{
  "message":<1-4096 chars>,
  "hash":<sha-512 hash of message>,
}
```

# CryptoPals
Solutions to the challenges located at https://cryptopals.com/

## Challenge
To create a secure communications program/algorithm

## Client Key Store Format
```
{
  'ClientID'  :<GUID>
  'RSAPrivate':<hex string>,
  'RSAPublic' :<hex string>,
  'HMACSecret':<hex string>,
  'AESSecret' :<hex string>,
  'OTPs'      :[{'id':<UUID>,'value':<4096 hex string>},
                {'id':<UUID>,'value':<4096 hex string>}]
}
```

## Encrypted Message Format
```
Encrypted message format:
messageID(plaintext).<encrypted message>.length.<SHA-512>

```

## Plaintext Message Format
```
Decrypted message format:

{
  "message":<1-4096 chars>,
  "hash":<sha-512 hash of message>,
}
```

## Comms API
```
{
  'userid':<userid>,
  'action':'new'|'del'|'getone'|'getall',
  'query':{'msgid':<messageID>}|{'usrid':<userID>},
  'message':{'msgid':<messageID>,'message':<message>}
}
```

## Notes
Zero knowledge system (computer has zero knowledge of the private keys and messages)
PK Cryptography
Two factor keys on both sides
Symmetric keys exchanged via PK
HMAC keys exchanged at the same time
One time pad used to encrypt communications
OTP keys are used for one session and then purged
Key size starts at 32,768 bits or 4096 characters
MessageID is SHA-512 hash of the key GUID

# This is under development.
# This software now seems reasonably secure.
# You still use this software at your own risk.
# This documentation is currently not valid.
# When the first release is published, documentation will be finished.

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

## Secure Communication
1. Encrypted server communication
2. Exchange public keys
3. Server generates aes key
4. Sends key to client rsa encrypted
5. Client generates one time pad
6. Sends to server aes encrypted
7. Client and server use otp to communicate
8. Keys are purged on disconnect

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

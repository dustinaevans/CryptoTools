def pad(data,length):
    data = data.encode()
    padlen = length - len(data)
    padval = chr(padlen).encode()
    padding = padval*padlen
    return data+padding

print(pad("YELLOW SUBMARINE",20))

def encrypt(text, key = int(3)):
    passwd = ''
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            passwd += chr((ord(char) + key -65) %26 +65)
        else:
            passwd += chr((ord(char) + key - 97) %26 +97)
    return passwd


def decrypted(text, key = int(3)):
    passwd = ''
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            passwd += chr((ord(char) - key - 65) % 26 + 65)
        else:
            passwd += chr((ord(char) - key - 97) % 26 + 97)

    return passwd







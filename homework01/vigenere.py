def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    if len(keyword) < len(plaintext):
        j = 0
        x = len(keyword)
        for i in plaintext:
            if j >= x:
                keyword += keyword[j % x]
            j += 1

    for k in range(len(plaintext)):
        i = plaintext[k]
        shift = ord(keyword[k]) % 65 if 65 <= ord(keyword[k]) <= 90 else ord(keyword[k]) % 97
        if 65 <= ord(i) <= 90:
            if ord(i) + shift > 90:
                ciphertext += chr((ord(i) + shift) % 90 + 64)
            else:
                ciphertext += chr(ord(i) + shift)
        elif 97 <= ord(i) <= 122:
            if ord(i) + shift > 122:
                ciphertext += chr((ord(i) + shift) % 122 + 96)
            else:
                ciphertext += chr(ord(i) + shift)
        else:
            ciphertext += i

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    if len(keyword) < len(ciphertext):
        j = 0
        x = len(keyword)
        for i in ciphertext:
            if j >= x:
                keyword += keyword[j % x]
            j += 1

    for k in range(len(ciphertext)):
        i = ciphertext[k]
        shift = ord(keyword[k]) % 65 if 65 <= ord(keyword[k]) <= 90 else ord(keyword[k]) % 97
        if 65 <= ord(i) <= 90:
            if ord(i) - shift < 65:
                plaintext += chr(ord(i) - shift + 26)
            else:
                plaintext += chr(ord(i) - shift)
        elif 97 <= ord(i) <= 122:
            if ord(i) - shift < 97:
                plaintext += chr(ord(i) - shift + 26)
            else:
                plaintext += chr(ord(i) - shift)
        else:
            plaintext += i

    return plaintext

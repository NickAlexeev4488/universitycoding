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
        key_length = len(keyword)
        for i in range(len(plaintext)):
            if i >= key_length:
                keyword += keyword[i % key_length]

    for k in range(len(plaintext)):
        letter = plaintext[k]
        shift = ord(keyword[k]) % ord("A") if ord("A") <= ord(keyword[k]) <= ord("Z") else ord(keyword[k]) % ord("a")
        if ord("A") <= ord(letter) <= ord("Z"):
            if ord(letter) + shift > ord("Z"):
                ciphertext += chr((ord(i) + shift) % ord("Z") + ord("A") - 1)
            else:
                ciphertext += chr(ord(i) + shift)
        elif ord("a") <= ord(letter) <= ord("z"):
            if ord(letter) + shift > ord("z"):
                ciphertext += chr((ord(letter) + shift) % ord("z") + ord("a") - 1)
            else:
                ciphertext += chr(ord(letter) + shift)
        else:
            ciphertext += letter

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
        value_length = 0
        keyword_length = len(keyword)
        for i in ciphertext:
            if value_length >= keyword_length:
                keyword += keyword[value_length % keyword_length]
            value_length += 1

    for k in range(len(ciphertext)):
        i = ciphertext[k]
        shift = ord(keyword[k]) % ord("A") if ord("A") <= ord(keyword[k]) <= ord("Z") else ord(keyword[k]) % ord("a")
        if ord("A") <= ord(i) <= ord("Z"):
            if ord(i) - shift < ord("A"):
                plaintext += chr(ord(i) - shift + ord("Z") - ord("A"))
            else:
                plaintext += chr(ord(i) - shift)
        elif ord("a") <= ord(i) <= ord("z"):
            if ord(i) - shift < ord("a"):
                plaintext += chr(ord(i) - shift + ord("z") - ord("a"))
            else:
                plaintext += chr(ord(i) - shift)
        else:
            plaintext += i

    return plaintext

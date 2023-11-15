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
        value_length = 0
        keyword_length = len(keyword)
        for i in plaintext:
            if value_length >= keyword_length:
                keyword += keyword[value_length % keyword_length]
            value_length += 1

    for k in range(len(plaintext)):
        letter = plaintext[k]
        shift = ord(keyword[k]) % 65 if 65 <= ord(keyword[k]) <= 90 else ord(keyword[k]) % 97
        if ord("A") <= ord(letter) <= ord("Z"):
            if ord(letter) + shift > ord("Z"):
                ciphertext += chr((ord(letter) + shift) % ord("Z") + ord("A") - 1)
            else:
                ciphertext += chr(ord(letter) + shift)
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
        letter = ciphertext[k]
        shift = ord(keyword[k]) % 65 if 65 <= ord(keyword[k]) <= 90 else ord(keyword[k]) % 97
        if ord("A") <= ord(letter) <= ord("Z"):
            if ord(letter) - shift < ord("A"):
                plaintext += chr(ord(letter) - shift + ord("Z") - ord("A") + 1)
            else:
                plaintext += chr(ord(letter) - shift)
        elif ord("a") <= ord(letter) <= ord("z"):
            if ord(letter) - shift < ord("a"):
                plaintext += chr(ord(letter) - shift + ord("z") - ord("a") + 1)
            else:
                plaintext += chr(ord(letter) - shift)
        else:
            plaintext += letter

    return plaintext

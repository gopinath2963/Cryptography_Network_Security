# vignere_cipher.py
import string

def generate_key(text, key):
    """Generate a key of the same length as the text."""
    key = key.upper()
    key_length = len(key)
    repeated_key = (key * (len(text) // key_length + 1))[:len(text)]
    return repeated_key

def encrypt_vigenere(plaintext, key):
    """Encrypt using Vigenère cipher."""
    plaintext = plaintext.upper().replace(" ", "")
    key = generate_key(plaintext, key)
    ciphertext = []
    alphabet = string.ascii_uppercase
    steps = []

    steps.append(f"Plaintext: {plaintext}")
    steps.append(f"Key: {key}")

    for i, (p, k) in enumerate(zip(plaintext, key)):
        if p in alphabet:
            p_idx = alphabet.index(p)
            k_idx = alphabet.index(k)
            c_idx = (p_idx + k_idx) % 26
            c = alphabet[c_idx]
            ciphertext.append(c)
            steps.append(f"Position {i+1}: {p}({p_idx}) + {k}({k_idx}) = {c}({c_idx})")
        else:
            ciphertext.append(p)  # Keep non-alphabetic characters
            steps.append(f"Position {i+1}: {p} (non-alphabetic, kept as is)")

    result = ''.join(ciphertext)
    steps.append(f"Ciphertext: {result}")
    return result, steps

def decrypt_vigenere(ciphertext, key):
    """Decrypt using Vigenère cipher."""
    ciphertext = ciphertext.upper().replace(" ", "")
    key = generate_key(ciphertext, key)
    plaintext = []
    alphabet = string.ascii_uppercase
    steps = []

    steps.append(f"Ciphertext: {ciphertext}")
    steps.append(f"Key: {key}")

    for i, (c, k) in enumerate(zip(ciphertext, key)):
        if c in alphabet:
            c_idx = alphabet.index(c)
            k_idx = alphabet.index(k)
            p_idx = (c_idx - k_idx) % 26
            p = alphabet[p_idx]
            plaintext.append(p)
            steps.append(f"Position {i+1}: {c}({c_idx}) - {k}({k_idx}) = {p}({p_idx})")
        else:
            plaintext.append(c)  # Keep non-alphabetic characters
            steps.append(f"Position {i+1}: {c} (non-alphabetic, kept as is)")

    result = ''.join(plaintext)
    steps.append(f"Plaintext: {result}")
    return result, steps
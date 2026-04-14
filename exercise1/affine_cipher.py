# affine_cipher.py
from .crypto_utils import char_to_index, index_to_lower_char, index_to_upper_char

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b."""
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Find the modular inverse of a modulo m using Extended Euclidean Algorithm."""
    m0, y, x = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        y, x = x - q * y, y
    if x < 0:
        x += m0
    return x

def validate_keys(a, b):
    """Validate affine cipher keys."""
    try:
        a_val = int(a)
        b_val = int(b)
    except ValueError:
        raise ValueError("Keys must be integers.")

    if gcd(a_val, 26) != 1:
        raise ValueError("Key 'a' must be coprime with 26 (gcd(a, 26) = 1).")

    if b_val < 0 or b_val > 25:
        raise ValueError("Key 'b' must be between 0 and 25.")

    return a_val, b_val

def encrypt_affine(plaintext, a, b):
    """Encrypt using Affine cipher: C = (a * P + b) mod 26"""
    a_val, b_val = validate_keys(a, b)
    result = []
    steps = []

    steps.append(f"Encryption formula: C = ({a_val} × P + {b_val}) mod 26")
    steps.append(f"Keys: a = {a_val}, b = {b_val}")
    steps.append("")

    for i, ch in enumerate(plaintext):
        idx = char_to_index(ch)
        if idx == -1:
            result.append(ch)
            steps.append(f"Character '{ch}' at position {i+1}: Non-alphabetic, unchanged")
        else:
            encrypted_idx = (a_val * idx + b_val) % 26
            encrypted_char = index_to_upper_char(encrypted_idx)
            result.append(encrypted_char)
            steps.append(f"Character '{ch}' (P={idx}) → '{encrypted_char}' (C={encrypted_idx})")
            steps.append(f"  Calculation: ({a_val} × {idx} + {b_val}) mod 26 = {encrypted_idx}")

    return "".join(result), steps

def decrypt_affine(ciphertext, a, b):
    """Decrypt using Affine cipher: P = a^(-1) * (C - b) mod 26"""
    a_val, b_val = validate_keys(a, b)
    a_inv = mod_inverse(a_val, 26)
    result = []
    steps = []

    steps.append(f"Decryption formula: P = {a_inv} × (C - {b_val}) mod 26")
    steps.append(f"Keys: a = {a_val}, b = {b_val}, a^(-1) = {a_inv}")
    steps.append("")

    for i, ch in enumerate(ciphertext):
        idx = char_to_index(ch)
        if idx == -1:
            result.append(ch)
            steps.append(f"Character '{ch}' at position {i+1}: Non-alphabetic, unchanged")
        else:
            decrypted_idx = (a_inv * (idx - b_val)) % 26
            decrypted_char = index_to_lower_char(decrypted_idx)
            result.append(decrypted_char)
            steps.append(f"Character '{ch}' (C={idx}) → '{decrypted_char}' (P={decrypted_idx})")
            steps.append(f"  Calculation: {a_inv} × ({idx} - {b_val}) mod 26 = {decrypted_idx}")

    return "".join(result), steps
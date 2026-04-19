from Crypto.Cipher import DES


def cmac_des_with_steps(message, key, nbits):
    steps = {
        'input_processing': {},
        'padding': {},
        'encryption': {},
        'final_processing': {},
        'final_cmac': None
    }

    # Step 1: Input Processing
    original_message = message
    if isinstance(message, str):
        message = message.encode()
        steps['input_processing']['message_encoding'] = f"Converted string '{original_message}' to bytes: {message.hex()}"

    original_key = key
    if isinstance(key, str):
        try:
            key = bytes.fromhex(key)
            steps['input_processing']['key_processing'] = f"Parsed hex key '{original_key}' to bytes: {key.hex()}"
        except ValueError:
            key = key.encode('utf-8')
            steps['input_processing']['key_processing'] = f"Converted text key '{original_key}' to bytes: {key.hex()}"

    if not isinstance(key, (bytes, bytearray)):
        raise TypeError('Key must be bytes or a string.')

    if len(key) < 8:
        key = key.ljust(8, b'\x00')
        steps['input_processing']['key_padding'] = f"Padded key to 8 bytes: {key.hex()}"
    elif len(key) > 8:
        key = key[:8]
        steps['input_processing']['key_truncation'] = f"Truncated key to 8 bytes: {key.hex()}"

    steps['input_processing']['final_key'] = f"Final DES key: {key.hex()}"

    # Step 2: Padding
    original_len = len(message)
    padding_len = 8 - (len(message) % 8)
    if padding_len != 8:
        message += b'\x80' + b'\x00' * (padding_len - 1)
        steps['padding']['padding_applied'] = f"Added {padding_len} bytes of padding (0x80 + {padding_len-1} x 0x00)"
    else:
        steps['padding']['no_padding'] = "Message length is multiple of 8, no padding needed"

    steps['padding']['padded_message'] = f"Padded message: {message.hex()}"
    steps['padding']['message_blocks'] = [message[i:i+8].hex() for i in range(0, len(message), 8)]

    # Step 3: CBC Encryption
    cipher = DES.new(key, DES.MODE_CBC, iv=b'\x00' * 8)
    ciphertext = cipher.encrypt(message)

    steps['encryption']['iv'] = "0000000000000000"
    steps['encryption']['mode'] = "CBC"
    steps['encryption']['ciphertext'] = ciphertext.hex()
    steps['encryption']['ciphertext_blocks'] = [ciphertext[i:i+8].hex() for i in range(0, len(ciphertext), 8)]

    # Step 4: Take last block
    last_block = ciphertext[-8:]
    steps['final_processing']['last_block'] = f"Last ciphertext block: {last_block.hex()}"

    # Step 5: Convert to binary
    binary = bin(int.from_bytes(last_block, 'big'))[2:].zfill(64)
    steps['final_processing']['binary_conversion'] = f"Binary representation: {binary}"

    # Step 6: Truncate
    truncated = binary[:nbits]
    steps['final_processing']['truncation'] = f"Truncated to {nbits} bits: {truncated}"

    # Step 7: Convert to hex
    cmac = hex(int(truncated, 2))[2:].zfill(nbits // 4)
    steps['final_cmac'] = cmac

    return steps


def cmac_des(message, key, nbits):
    # For backward compatibility, keep the simple function
    steps = cmac_des_with_steps(message, key, nbits)
    return steps['final_cmac']
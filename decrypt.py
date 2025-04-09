#!/usr/bin/env python3

import sys

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def decrypt(ciphertext, key):
    """Decrypt the Vigenère cipher with the given key."""
    plaintext = ''
    key = key.upper()
    key_idx = 0
    for c in ciphertext:
        if c in LETTERS:
            c_idx = LETTERS.index(c)
            k_idx = LETTERS.index(key[key_idx % len(key)])
            p_idx = (c_idx - k_idx) % 26
            plaintext += LETTERS[p_idx]
            key_idx += 1
        else:
            plaintext += c
    return plaintext

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 decrypt.py <ciphertext_file> <key_file>")
        sys.exit(1)

    # Read ciphertext
    with open(sys.argv[1], 'r') as f:
        ciphertext = f.read().upper()

    # Read key
    with open(sys.argv[2], 'r') as f:
        key = f.read().strip()

    # Clean ciphertext (remove non-letters)
    ciphertext_clean = ''.join(c for c in ciphertext if c in LETTERS)
    print("Cleaned ciphertext:", ciphertext_clean[:100], "...")

    # Decrypt
    plaintext = decrypt(ciphertext_clean, key)
    print(f"Decrypted text: {plaintext[:100]}...")
    with open("plaintext.txt", "w") as f:
        f.write(plaintext)
    print("Decrypted text saved to plaintext.txt")

if __name__ == "__main__":
    main()

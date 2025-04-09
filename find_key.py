#!/usr/bin/env python3

import sys
from collections import Counter

# Constants
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16  # Maximum key length to try
ENGLISH_IC = 0.065  # Expected IC for English text

def clean_text(text):
    """Remove non-letters and convert to uppercase."""
    return ''.join(c for c in text.upper() if c in LETTERS)

def calculate_ic(text):
    """Calculate the Index of Coincidence for a given text."""
    length = len(text)
    if length < 2:
        return 0.0
    freqs = Counter(text)
    ic = sum(n * (n - 1) for n in freqs.values()) / (length * (length - 1))
    return ic

def find_key_length(ciphertext):
    """Find the most likely key length using Index of Coincidence."""
    best_length = 0
    best_ic = 0.0
    for length in range(1, MAX_KEY_LENGTH + 1):
        total_ic = 0.0
        for i in range(length):
            subtext = ciphertext[i::length]
            ic = calculate_ic(subtext)
            total_ic += ic
        avg_ic = total_ic / length if length > 0 else 0
        print(f"Key length {length}: IC = {avg_ic:.4f}")
        if abs(avg_ic - ENGLISH_IC) < abs(best_ic - ENGLISH_IC):
            best_ic = avg_ic
            best_length = length
    print(f"Most likely key length: {best_length}")
    return best_length

def find_key(ciphertext, key_length):
    """Find the key using frequency analysis."""
    key = ''
    for i in range(key_length):
        subtext = ciphertext[i::key_length]
        freqs = Counter(subtext)
        # Find the most frequent letter
        most_freq = max(freqs.items(), key=lambda x: x[1])[0]
        # Assume the most frequent letter is 'E'
        most_freq_idx = LETTERS.index(most_freq)
        e_idx = LETTERS.index('E')
        key_letter_idx = (most_freq_idx - e_idx) % 26
        key_letter = LETTERS[key_letter_idx]
        key += key_letter
    return key

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 find_key.py <ciphertext_file>")
        sys.exit(1)

    # Read ciphertext
    with open(sys.argv[1], 'r') as f:
        ciphertext = f.read()

    # Clean the ciphertext
    ciphertext_clean = clean_text(ciphertext)
    print("Cleaned ciphertext:", ciphertext_clean[:100], "...")

    # Find key length
    key_length = find_key_length(ciphertext_clean)

    # Find key
    key = find_key(ciphertext_clean, key_length)
    print(f"Found key: {key}")

    # Save the key to a file
    with open("key.txt", "w") as f:
        f.write(key)
    print("Key saved to key.txt")

if __name__ == "__main__":
    main()

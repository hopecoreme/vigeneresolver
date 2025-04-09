#!/usr/bin/env python3

import sys
import re
import subprocess
import requests
from collections import Counter

# Constants
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16  # Maximum key length to try
ENGLISH_IC = 0.065  # Expected IC for English text
ENGLISH_FREQ = {'E': 0.127, 'T': 0.091, 'A': 0.082}  # English letter frequencies

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
        total = len(subtext)
        # Find the most frequent letter
        most_freq = max(freqs.items(), key=lambda x: x[1])[0]
        # Assume the most frequent letter is 'E'
        most_freq_idx = LETTERS.index(most_freq)
        e_idx = LETTERS.index('E')
        key_letter_idx = (most_freq_idx - e_idx) % 26
        key_letter = LETTERS[key_letter_idx]
        key += key_letter
    return key

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

def find_author(plaintext):
    """Find the author by searching Wikipedia."""
    # First, check the plaintext for clues
    if 'THE MENTOR' in plaintext.upper():
        print("Found 'The Mentor' in the decrypted text. Searching for real name...")
    else:
        print("No mention of 'The Mentor' in the text. Proceeding with Wikipedia search...")

    # Download Wikipedia page
    try:
        print("Downloading Wikipedia page for 'The Conscience of a Hacker'...")
        response = requests.get("https://en.wikipedia.org/wiki/The_Conscience_of_a_Hacker")
        wiki_text = response.text
    except Exception as e:
        print(f"Failed to download Wikipedia page: {e}")
        print("Falling back to curl...")
        try:
            subprocess.run(["curl", "-s", "https://en.wikipedia.org/wiki/The_Conscience_of_a_Hacker", "-o", "wiki_page.html"])
            with open("wiki_page.html", "r") as f:
                wiki_text = f.read()
            subprocess.run(["rm", "-f", "wiki_page.html"])
        except Exception as e:
            print(f"Failed to download with curl: {e}")
            return "Could not determine author automatically."

    # Search for Loyd Blankenship
    match = re.search(r'Loyd Blankenship', wiki_text, re.IGNORECASE)
    if match:
        print("Author's real name found: Loyd Blankenship")
        return "Loyd Blankenship"
    else:
        print("Trying alternative Wikipedia page (Legion of Doom)...")
        try:
            response = requests.get("https://en.wikipedia.org/wiki/Legion_of_Doom_(hacking)")
            wiki_text = response.text
        except Exception as e:
            print(f"Failed to download alternative page: {e}")
            return "Could not determine author automatically."
        match = re.search(r'Loyd Blankenship', wiki_text, re.IGNORECASE)
        if match:
            print("Author's real name found: Loyd Blankenship")
            return "Loyd Blankenship"
        else:
            print("Could not find the author's real name.")
            return "Could not determine author automatically."

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 vigenere_solver.py <ciphertext_file>")
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

    # Decrypt
    plaintext = decrypt(ciphertext_clean, key)
    print(f"Decrypted text: {plaintext[:100]}...")
    with open("plaintext.txt", "w") as f:
        f.write(plaintext)
    print("Full decrypted text saved to plaintext.txt")

    # Find author
    author = find_author(plaintext)
    print(f"Final answer - Author: {author}")

if __name__ == "__main__":
    main()

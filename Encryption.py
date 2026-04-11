# Reads user input
from re import S
from pathlib import Path
# Collect shift values from the user
try:
    shift1 = int(input("Enter the first shift value: "))
    shift2 = int(input("Enter the second shift value: "))
    
    except ValueError:
        raise SystemExit("Shift values must be an error.")


def encrypt_char(ch):
    if ch.islower():
        index = ord(ch) - ord('a')
        if index <= 12: # if character is a-m, shift by shift1 * shift2. wraps around alphabet when necessary
            new_index = index + (shift1 * shift2) % 26
        else: # if character is n-z, shift by shift1 - shift2. wraps around alphabet when necessary
            new_index = index - (shift1 + shift2) %26
        return chr(new_index + ord('a'))

    elif ch.isupper():
        index = ord(ch) - ord('A')
        if index <= 12: # if character is A-M, subtracts by shift1. wraps around alphabet when necessary
            new_index = (index - shift1) % 26
        else: # if character is N-Z, shift by shift^2. wraps around alphabet when necessary
            new_index = (index + shift2 ** 2) % 26
        return chr(new_index + ord('A'))
    return ch

with open("raw_text.txt", 'r', encoding="utf-8") as infile:
    content = infile.read()
 
encrypted = "".join(encrypt_char(ch) for ch in content)
 
with open("encrypted_text.txt", 'w', encoding="utf-8") as outfile:
    outfile.write(encrypted)
 
print("Done! Encrypted content saved to encrypted_text.txt");
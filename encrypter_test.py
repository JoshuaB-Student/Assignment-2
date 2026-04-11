shift1 = int(input("Enter shift1: ")) # Collects shift inputs from user
shift2 = int(input("Enter shift2: "))
 
with open("raw_text.txt", "r") as f: # Reads the raw text from the file named "raw_text.txt"
    raw = f.read()
 
result = []
for ch in raw:
    if ch.isupper():
        idx = ord(ch) - ord('A')
        if idx <= 12:  # A-M: shift backward by shift1
            new_idx = (idx - shift1) % 26
        else:          # N-Z: shift forward by shift2^2
            new_idx = (idx + shift2 ** 2) % 26
        result.append(chr(new_idx + ord('A')))
    elif ch.islower():
        idx = ord(ch) - ord('a')
        if idx <= 12:  # a-m: shift forward by shift1 * shift2
            new_idx = (idx + shift1 * shift2) % 26
        else:          # n-z: shift backward by shift1 + shift2
            new_idx = (idx - (shift1 + shift2)) % 26
        result.append(chr(new_idx + ord('a')))
    else:
        result.append(ch)
 
with open("encrypted_text.txt", "w") as f: # Inputs the encrypted text into a new file named "encrypted_text.txt"
    f.write(''.join(result))

def verify():
    with open("raw_text.txt", "r") as f:
        original = f.read()

    with open("decrypted_text.txt", "r") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Verification successful! Decrypted text matches the original.")
    else:
        mismatch_count = sum(1 for a, b in zip(original, decrypted) if a != b)
        print(f"Verification FAILED - {mismatch_count} character(s) do not match.")
        for i, (a, b) in enumerate(zip(original, decrypted)):
            if a != b:
                print(f"  First mismatch at position {i}: "
                      f"original={repr(a)}, decrypted={repr(b)}")

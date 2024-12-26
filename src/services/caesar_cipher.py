def preprocess_text(text):
    """Preprocess text by keeping all characters as literals"""
    return text.encode('unicode_escape').decode('utf-8')

def caesar_cipher(text, alphabet, shift, mode='encrypt', case_strategy='strict', ignore_foreign=False):
    """Encrypts or decrypts text using the Caesar cipher."""
    result = ""
    
    # Create case-specific alphabets if needed
    if case_strategy in ['maintain', 'ignore']:
        lower_alphabet = alphabet.lower()
        upper_alphabet = alphabet.upper()
    
    for char in text:
        if case_strategy == 'strict':
            if char in alphabet:
                index = alphabet.index(char)
                if mode == 'encrypt':
                    new_index = (index + shift) % len(alphabet)
                else:
                    new_index = (index - shift) % len(alphabet)
                result += alphabet[new_index]
            elif not ignore_foreign:
                result += char
                
        elif case_strategy == 'maintain':
            if char.lower() in lower_alphabet:
                index = lower_alphabet.index(char.lower())
                if mode == 'encrypt':
                    new_index = (index + shift) % len(alphabet)
                else:
                    new_index = (index - shift) % len(alphabet)
                if char.isupper():
                    result += upper_alphabet[new_index]
                else:
                    result += lower_alphabet[new_index]
            elif not ignore_foreign:
                result += char
                
        elif case_strategy == 'ignore':
            char_lower = char.lower()
            if char_lower in lower_alphabet:
                index = lower_alphabet.index(char_lower)
                if mode == 'encrypt':
                    new_index = (index + shift) % len(alphabet)
                else:
                    new_index = (index - shift) % len(alphabet)
                result += lower_alphabet[new_index]
            elif not ignore_foreign:
                result += char
                
    return result

def encode_key(key, alphabet):
    """Encodes the key to a string using the given alphabet (base conversion)."""
    base = len(alphabet)
    if key == 0:
        return alphabet[0]
    
    digits = []
    while key:
        digits.append(alphabet[key % base])
        key //= base
    return "".join(digits[::-1])  # Reverse to get correct order

def decode_key(encoded_key, alphabet):
    """Decodes the key from a string to an integer."""
    base = len(alphabet)
    key = 0
    for char in encoded_key:
        key = key * base + alphabet.index(char)
    return key

def shift_alphabet(alphabet, shift):
    """Returns the shifted alphabet"""
    return alphabet[shift:] + alphabet[:shift]
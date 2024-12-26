import numpy as np
import matplotlib.pyplot as plt

def get_bin_char(c):
    x = [int(x) for x in bin(ord(c))[2:]]
    x = [0] * (7 - len(x)) + x
    return x

def get_bin_str(s):
    ret = []
    for c in s:
        ret += get_bin_char(c)
    ret += [0] * 7  # Add on null terminator "\0"
    return ret

def encode(image, message):
    x = get_bin_str(message)
    x = x + [0] * 7
    x = np.array(x, dtype=np.uint8)
    image_rounded = image - image % 2
    image_flat = image_rounded.flatten()
    image_flat[0:x.size] += x  # Adding in hidden bits
    return np.reshape(image_flat, image.shape)

def decode(image):
    places = np.array([2 ** (6 - i) for i in range(7)])
    image_flat = image.flatten()
    i = 0
    still_reading = True
    decoded_message = ""
    while still_reading:
        c = image_flat[i:i + 7] % 2
        c = np.sum(places * c)
        if c == 0:
            still_reading = False
        else:
            decoded_message += chr(c)
        i += 7
    return decoded_message
import numpy as np
from PIL import Image
from io import BytesIO

def load_image(path_or_bytes):
    """Load an image from path or bytes."""
    if isinstance(path_or_bytes, BytesIO):
        image = Image.open(path_or_bytes)
        return np.array(image)
    return np.array(Image.open(path_or_bytes))

def save_image(image, path):
    """Save the image to the specified path."""
    Image.fromarray(image).save(path)
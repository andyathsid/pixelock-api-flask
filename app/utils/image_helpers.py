import numpy as np
import skimage.io

def load_image(path):
    """Load an image from the specified path."""
    return skimage.io.imread(path)

def save_image(image, path):
    """Save the image to the specified path."""
    skimage.io.imsave(path, image)
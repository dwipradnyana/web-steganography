import numpy as np
import math
from PIL import Image

def calculate_psnr(original, modified):
    original = np.array(original)
    modified = np.array(modified)
    mse = np.mean((original - modified) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

original_image = Image.open("gray2.jpeg")
modified_image = Image.open("stego_gray2.jpeg")

psnr_value = calculate_psnr(original_image, modified_image)

print("PSNR:", psnr_value)

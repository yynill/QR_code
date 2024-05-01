import re
import json
from PIL import Image
import os
import random

# 21 * 21 (version 1 QRcode)
original_width = original_height = 21
upscale_factor = 20


def generateRandomString(length):
    return ''.join(random.choices(['0', '1', '2'], k=length))


# Finder Pattern: Consists of three large squares strategically placed to help the camera identify the orientation of the code quickly and accurately.
# Timer Pattern: Comprising the sequence "10101", this pattern aids in aligning the code correctly, particularly when it's distorted or warped.
# Dark Module: Positioned at the bottom-right corner of the finder pattern, this sole black module serves as a reference point for the code's positioning.
# Format Information (Pink): Encodes critical data such as Format Error Correction, Mask Pattern, and Correction Level, ensuring the accuracy and integrity of the encoded information.
# Data and Encoding Zones (Marked as '9'): These areas are designated for housing the actual data as well as encoding data, forming the core content of the QR code.

fixdedPattern = [
    """
    111111102999901111111
    100000102999901000001
    101110102999901011101
    101110102999901011101
    101110102999901011101
    100000102999901000001
    111111101010101111111
    000000002999900000000
    222222122999992222222
    999999099999999999999
    999999199999999999999
    999999099999999999999
    999999199999999999999
    000000001999999999999
    111111102999999999999
    100000102999999999999
    101110102999999999999
    101110102999999999999
    101110102999999999999
    100000102999999999999
    111111102999999999999
    """
]

fixdedPattern = "".join([line.strip()
                        for line in fixdedPattern[0].split('\n') if line.strip()])


def drawQR(binary_string):
    image = Image.new("RGB", (original_width,  original_height), "white")
    pixels = image.load()

    binary_list = [int(bit) for bit in binary_string]

    for i in range(len(binary_list)):
        x = i % original_width
        y = i // original_width

        # 0 - white - binary 0
        if binary_list[i] == 0:
            pixels[x, y] = (255, 255, 255)

        # 1 black - binary 1
        elif binary_list[i] == 1:
            pixels[x, y] = (0, 0, 0)

        # 2 - pink - formatting info
        elif binary_list[i] == 2:
            pixels[x, y] = (255, 182, 193)

        # 9 - gray - free square
        elif binary_list[i] == 9:
            pixels[x, y] = (210, 210, 210)

        # error
        else:
            pixels[x, y] = (255, 0, 0)

    return image


# QR codes use ISO-8859-1 to encode their byte strings
data_to_encode = "https://www.qrcode.com/"


qr_image = drawQR(fixdedPattern)

# Upscale the image
upscaled_qr_image = qr_image.resize(
    (original_width * upscale_factor, original_height * upscale_factor), Image.NEAREST)

upscaled_qr_image.show()

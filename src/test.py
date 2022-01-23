import math
import cv2
from cv2 import resize
import numpy as np


MAX_WORKING_LENGTH = 830  # Length of working area (mm)
PAINT_DOT_SIZE = 3  # Size (length/width) of paint dot; must be ODD (mm)
MOVEMENT_SPEED = 1200  # Movement speed in mm/min

# Resize image so largest axis becomes MAX_WORKING_LENGTH
def resize_image(img):
    # Use largest axis for resizing image
    largest_axis = 0
    if img.shape[1] > img.shape[0]:
        largest_axis = 1

    multiplication_factor = MAX_WORKING_LENGTH / img.shape[largest_axis]

    return cv2.resize(
        img,
        (
            math.floor(img.shape[1] * multiplication_factor),
            math.floor(img.shape[0] * multiplication_factor),
        ),
    )


# Downsample image according to PAINT_DOT_SIZE
def downsample_image(img):
    decrease_factor = PAINT_DOT_SIZE - 1
    new_img = img
    for _ in range(decrease_factor):
        # Blur image and downsample (Gaussian Pyramid)
        new_img = cv2.pyrDown(img)
    return new_img


# Creates gcode file from every pixel in the image (assumes image is already correctly sized)
def generate_gcode_file(img):
    with open("GCodeTest.gcode", "w") as file:
        # Setup
        file.write("G28 ;\n")  # Home all motors
        file.write("G90 ;\n")  # Absolute positioning mode
        file.write("G21 ;\n")  # Set units to mm

        y_counter = 0
        for y_displacement in range(img.shape[0]):
            file.write("G0 Y{} F{} ;\n".format(y_displacement, MOVEMENT_SPEED))

            # Compute range (prevent unnecessary movement to the other edge)
            if y_counter % 2 == 0:
                rangeToUse = range(img.shape[1])
            else:
                rangeToUse = range(img.shape[1], 0, -1)

            for x_displacement in rangeToUse:
                val = img[y_displacement, x_displacement]
                if val == 0:  # Values are 255 or 0
                    file.write("G0 X{} F{} ;\n".format(x_displacement, MOVEMENT_SPEED))
                    # Mark a dot
                    file.write("G1 Z{} F{} ;\n".format(-10, MOVEMENT_SPEED))
                    file.write("G1 Z{} F{} ;\n".format(0, MOVEMENT_SPEED))

        # Program finished; return to home position
        file.write("G28 ;\n")


img = cv2.imread("monkey.jpg")
print(img.shape)

resized_img = resize_image(img)
print(resized_img.shape)

_, black_white_img = cv2.threshold(
    cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY),
    128,
    255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU,
)

# downsampled_img = downsample_image(resized_img)
# print(downsampled_img.shape)

generate_gcode_file(black_white_img)

cv2.imshow("Image", img)
cv2.imshow("Black & White Image", black_white_img)
cv2.imshow("Resized Image", resized_img)
# cv2.imshow("Downsampled Image", downsampled_img)
cv2.waitKey(0)
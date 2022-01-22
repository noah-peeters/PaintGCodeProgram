import math
import cv2
import numpy as np


MAX_WORKING_LENGTH = 1000  # Length of working area (mm)
PAINT_DOT_SIZE = 3  # Size (length/width) of paint dot; must be ODD (mm)
MOVEMENT_SPEED = 1200  # Movement speed in mm/min

# Resize image to MAX_WORKING_LENGTH
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


# Creates gcode file from every pixel in the image
def generate_gcode_file(img):
    with open("GCodeTest.gcode", "x") as file:
        # Home all motors
        file.write("G28 ;\n")
        # Absolute positioning mode
        file.write("G90 ;\n")

        # Increment (keeping kernel size in mind)
        increment = PAINT_DOT_SIZE - 1

        for y_index in range(0, img.shape[0], increment):
            for x_index in range(0, img.shape[1], increment):
                x_displacement = x_index
                y_displacement = y_index

                # TODO: "Place" pixel in top-left or top-right of kernel and compute average color value from kernel

                # TODO: Compute displacement offset for GCode dot

                file.write(
                    "G1 X{} Y{} F{} ;\n".format(
                        x_displacement, y_displacement, MOVEMENT_SPEED
                    )
                )
        file.write("G28 ;\n")


img = cv2.imread("monkey.jpg")
print(img.shape)

_, black_white_img = cv2.threshold(
    cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
)

resized_img = resize_image(img)
print(resized_img.shape)

downsampled_img = downsample_image(resized_img)
print(downsampled_img.shape)

generate_gcode_file(downsampled_img)

cv2.imshow("Image", img)
cv2.imshow("Black & White Image", black_white_img)
cv2.imshow("Resized Image", resized_img)
cv2.imshow("Downsampled Image", downsampled_img)
cv2.waitKey(0)
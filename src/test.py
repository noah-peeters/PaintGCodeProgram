import math
import cv2
from httpx import patch

MAX_WORKING_LENGTH = 100  # Longest length of working area (mm)
PAINT_DOT_DIAMETER = 3  # Diameter of paint dot; must be ODD (mm)
MOVEMENT_SPEED = 1400  # Movement speed in mm/min (max is 1500)

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


# Get black/white pixel value for patch (count separate occurences and return most)
def get_pixel_patch_value(patch):
    blackCount = 0
    whiteCount = 0
    for y in range(PAINT_DOT_DIAMETER - 1):
        for x in range(PAINT_DOT_DIAMETER - 1):
            pixelValue = patch[y, x]
            if pixelValue == 0:
                blackCount += 1
            elif pixelValue == 255:
                whiteCount += 1

    # Return white on equal
    if blackCount > whiteCount:
        return 0
    else:
        return 1


# Creates gcode file from every pixel in the image (assumes image is already correctly sized)
def generate_gcode_file(img):
    with open("GCodeTest.gcode", "w") as file:
        # Setup
        file.write("G28 ;\n")  # Home all motors
        file.write("G90 ;\n")  # Absolute positioning mode
        file.write("G21 ;\n")  # Set units to mm

        increment = PAINT_DOT_DIAMETER - 1
        y_counter = 0
        for y_displacement in range(increment, img.shape[0], increment):
            file.write("G0 Y{} F{} ;\n".format(y_displacement, MOVEMENT_SPEED))

            # Compute range (prevent unnecessary movement to the other edge)
            if y_counter % 2 == 0:
                rangeToUse = range(increment, img.shape[1], increment)
            else:
                rangeToUse = range(img.shape[1], increment, -increment)

            for x_displacement in rangeToUse:
                patch_around_img = img[
                    y_displacement - increment : y_displacement + increment,
                    x_displacement - increment : x_displacement + increment,
                ]
                val = get_pixel_patch_value(patch_around_img)
                if val == 0:  # Values are 255 or 0
                    file.write("G0 X{} F{} ;\n".format(x_displacement, MOVEMENT_SPEED))
                    # Mark a dot
                    file.write("G1 Z{} F{} ;\n".format(-10, MOVEMENT_SPEED))
                    file.write("G1 Z{} F{} ;\n".format(0, MOVEMENT_SPEED))

        # Program finished; return to home position
        file.write("G28 ;\n")


img = cv2.imread("monkey.jpg")

resized_img = resize_image(img)

_, black_white_img = cv2.threshold(
    cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY),
    128,
    255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU,
)

generate_gcode_file(black_white_img)

cv2.imshow("Image", img)
cv2.imshow("Black & White Image", black_white_img)
cv2.imshow("Resized Image", resized_img)
# cv2.imshow("Downsampled Image", downsampled_img)
cv2.waitKey(0)
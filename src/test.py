import math
import cv2

MAX_WORKING_LENGTH = 350  # Longest length of working area (mm)
PAINT_DOT_DIAMETER = 3  # Diameter of paint dot; must be ODD (mm)
XY_MOVEMENT_SPEED = 3000  # Movement speed in mm/min
Z_MOVEMENT_SPEED = 1700
Z_AXIS_DOWN_POS = -49.5  # Z-axis down position (point on paper)
Z_AXIS_LIFT_UP = 2  # Z-axis lift up offset
GCODE_FILE_NAME = "MonkeyLogo"

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
    with open(GCODE_FILE_NAME + ".gcode", "w") as file:
        # Setup
        file.write("G28 ;\n")  # Home all motors
        file.write("G90 ;\n")  # Absolute positioning mode
        file.write("G21 ;\n")  # Set units to mm

        increment = PAINT_DOT_DIAMETER - 1
        y_counter = 0
        for y_displacement in range(increment, img.shape[0], increment):
            file.write("G0 Y{} F{} ;\n".format(y_displacement, XY_MOVEMENT_SPEED))

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
                    file.write(
                        "G0 X{} F{} ;\n".format(x_displacement, XY_MOVEMENT_SPEED)
                    )
                    # Mark a dot
                    file.write(
                        "G1 Z{} F{} ;\n".format(Z_AXIS_DOWN_POS, Z_MOVEMENT_SPEED)
                    )
                    file.write(
                        "G1 Z{} F{} ;\n".format(
                            Z_AXIS_DOWN_POS + Z_AXIS_LIFT_UP, Z_MOVEMENT_SPEED
                        )
                    )

        # Program finished; return to home position
        file.write("G28 ;\n")


img = cv2.imread("MonkeyLogo.jpg")

resized_img = resize_image(img)

_, black_white_img = cv2.threshold(
    cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY),
    128,
    255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU,
)

generate_gcode_file(black_white_img)

# cv2.imshow("Image", img)
# cv2.imshow("Black & White Image", black_white_img)
# cv2.imshow("Resized Image", resized_img)
cv2.waitKey(0)

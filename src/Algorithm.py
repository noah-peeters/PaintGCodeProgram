"""
Algorithm for generating G-code for image.
"""
import math
import cv2


class GenerateDots:
    image = None
    settings = {
        "MaxWorkingLength": 350,
        "DotDiameter": 3,
        "XY_Speed": 3000,
        "Z_Speed": 1700,
        "Z_AxisDownPos": -49.5,
        "Z_AxisLiftUp": 2,
    }

    def __init__(self):
        print("init")

    # Resize image so largest axis becomes MAX_WORKING_LENGTH
    def resize_image(self):
        # Use largest axis for resizing image
        largest_axis = 0
        if self.image.shape[1] > self.image.shape[0]:
            largest_axis = 1

        multiplication_factor = (
            self.settings["MaxWorkingLength"] / self.image.shape[largest_axis]
        )

        return cv2.resize(
            self.image,
            (
                math.floor(self.image.shape[1] * multiplication_factor),
                math.floor(self.image.shape[0] * multiplication_factor),
            ),
        )

    # Get black/white pixel value for patch (count separate occurences and return most)
    def get_pixel_patch_value(self, patch):
        blackCount = 0
        whiteCount = 0
        for y in range(self.settings["DotDiameter"] - 1):
            for x in range(self.settings["DotDiameter"] - 1):
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
    def generate_gcode_file(self, filename):
        with open(filename, "w") as file:
            # Setup
            file.write("G28 ;\n")  # Home all motors
            file.write("G90 ;\n")  # Absolute positioning mode
            file.write("G21 ;\n")  # Set units to mm

            increment = self.settings["DotDiameter"] - 1
            y_counter = 0
            for y_displacement in range(increment, self.image.shape[0], increment):
                file.write(
                    "G0 Y{} F{} ;\n".format(y_displacement, self.settings["XY_Speed"])
                )

                # Compute range (prevent unnecessary movement to the other edge)
                if y_counter % 2 == 0:
                    rangeToUse = range(increment, self.image.shape[1], increment)
                else:
                    rangeToUse = range(self.image.shape[1], increment, -increment)

                for x_displacement in rangeToUse:
                    patch_around_img = self.image[
                        y_displacement - increment : y_displacement + increment,
                        x_displacement - increment : x_displacement + increment,
                    ]
                    val = self.get_pixel_patch_value(patch_around_img)
                    if val == 0:  # Values are 255 or 0
                        file.write(
                            "G0 X{} F{} ;\n".format(
                                x_displacement, self.settings["XY_Speed"]
                            )
                        )
                        # Mark a dot
                        file.write(
                            "G1 Z{} F{} ;\n".format(
                                self.settings["Z_AxisDownPos"], self.settings["Z_Speed"]
                            )
                        )
                        file.write(
                            "G1 Z{} F{} ;\n".format(
                                self.settings["Z_AxisDownPos"]
                                + self.settings["Z_AxisLiftUp"],
                                self.settings["Z_Speed"],
                            )
                        )
            # Program finished; return to home position
            file.write("G28 ;\n")

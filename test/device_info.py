import os
import sys
import logging
from aml_cv.logger import Logger

root_dir = '/home/mohit/Documents/_Github/GreenGrass/aml_cv/'
# os.chdir(root_dir)
sys.path.append(root_dir)

logger = Logger(
    log_level=logging.INFO, log_files=[],
    truncate_log_files=True, output_to_stdout=True
)

import cv2
import time
from aml_cv.color.selection_and_conversion import (
    Color, color_to_rgb, get_approx_hsv_value_limit_from_rgb_value
)
from aml_cv.color.thresholding import ColorThreshold, grayscale_n_levels
from aml_cv.color.transfer import ColorTransfer
from aml_cv.image import view_image

# ============================================================================ #
# Script 1: Color Selection and Conversion
# ---------------------------------------------------------------------------- #

# Random color selection
clr = Color().random()
logger.info(f"In Hex: {clr.hex} \t In RGB: {clr.rgb} \t In HLS: {clr.hls}")

# Color profile conversion
color = "#999999"
logger.info(f"From Hex `{color}` to RGB `{clr.create(color).rgb}` or HLS `{clr.create(color).hls}`")
color = (153, 153, 153)
logger.info(f"From RGB `{color}` to Hex `{clr.create(color).hex}` or HLS `{clr.create(color).hls}`")
color = (0.0, 0.6, 0.0)
logger.info(f"From HLS `{color}` to RGB `{clr.create(color).rgb}` or Hex `{clr.create(color).hex}`")

# Create folor from string
logger.info("{} {} {} | {}".format(
    Color.rgb_from_string("Hello:"),
    Color.rgb_from_string("Hel"),
    Color.rgb_from_string("hel"),
    Color.rgb_from_string("Moh")
))

# Color conversion of frame
img_bgr = cv2.imread("../sample_data/images/football_player_down.jpeg")
img_rgb = color_to_rgb(img_bgr, input_color_space="bgr")
view_image(img_bgr)
view_image(img_rgb)

# Get approx lower and upper limit of HSV color value
get_approx_hsv_value_limit_from_rgb_value([155, 155, 155])

# ============================================================================ #


# ============================================================================ #
# Script 2: Color Thresholding
# ---------------------------------------------------------------------------- #
img_rgb = color_to_rgb(cv2.imread("../sample_data/images/leaf.jpeg"), "bgr")
_, _ = ColorThreshold.generate_mask_and_output(
    img_rgb, (0,0,0), (0, 255, 100), input_color_space="rgb", visual_in_rgb=True
)

img_rgb = color_to_rgb(cv2.imread("../sample_data/images/sunglasses_beach_women.jpeg"), "bgr")
_, _ = ColorThreshold.generate_mask_and_output(
    img_rgb, (0,0,0), (242, 208, 138), input_color_space="rgb", visual_in_rgb=True
)

# lower, upper = [10, 10, 0], [255, 255, 45]
# im = cv2.imread("/Users/mohitrajput/Pictures/vlcsnap-2020-06-13-03h22m29s867.png")
# image_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
# _,_ = ColorThreshold.generate_mask_and_output(image_rgb, lower, upper, input_color_space="rgb")

view_image(grayscale_n_levels(img_rgb, n_levels=3))
# ============================================================================ #


# ============================================================================ #
# Script 3: Color Transfer
# ---------------------------------------------------------------------------- #
# source = cv2.imread("../sample_data/images/ombre_circle_grayscale.png")
# target = cv2.imread("../sample_data/images/fashion_male_female.jpg")
source = cv2.imread("../sample_data/images/football_player_down.jpeg")
target = cv2.imread("../sample_data/images/dance_steps.jpg")
transfer = ColorTransfer(source, target, clip=False, preserve_paper=False, output_path=None).run()
view_image(source, show_in_rgb=True, input_color_space="bgr")
view_image(target, show_in_rgb=True, input_color_space="bgr")
view_image(transfer, show_in_rgb=True, input_color_space="bgr")

# ============================================================================ #

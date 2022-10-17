ELEMENTS_DIR = "input/elements/"
INPUT_DIR = "input/base_variant/"
OUTPUT_DIR = "output_stage1_hdmi_panel/"
TEMP_DIR = "temp/"


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


class DrillSettings:
    format = [3, 3]
    units = "metric"
    zeros = "trailing"
    notation = "absolute"
    zero_suppression = "leading"

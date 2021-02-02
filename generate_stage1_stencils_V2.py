
# NOTES
# =====
#
# export eagle CAM gerber: for top cream normally
# export eagle CAM gerber: for top boardoutline normally
# export eagle CAM gerber: for bottom cream "mirrored"
# export eagle CAM gerber: for bottom boardoutline "mirrored" - thats important as its not the same result as boardoutline without flipping
# rotate mirrored MB and PB layers CW and the non flipped MB and PB layers CCW via script: rotate_for_stencil.sh
# run this script
#
# ====================================================

import os
import time
from datetime import date

import ezdxf
import gerberex
from HersheyFonts import HersheyFonts
from gerberex import DrillComposition
from gerberex import GerberComposition
from tabulate import tabulate

from frame_generator import generate_pcb_frame, generate_pcb_bridges, generate_outer_frame

ELEMENTS_DIR = "input/elements/"
INPUT_DIR = "input/tele_variant/"
OUTPUT_DIR = "output_stage1/"
TEMP_DIR = "temp/"

cutout_width = 2.54  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()

board_info_doc = ezdxf.new('R2010')
board_info_msp = board_info_doc.modelspace()

today = date.today()


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"

board_outline_context = GerberComposition(settings=GerberSettings)
cream_top_layer_context = GerberComposition(settings=GerberSettings)
cream_bot_layer_context = GerberComposition(settings=GerberSettings)
engrave_top_layer_context = GerberComposition(settings=GerberSettings)
engrave_bot_layer_context = GerberComposition(settings=GerberSettings)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)


pcb_info = []


def remove_gerber_outline(board_outline):
    delete_start = -1
    delete_end = -1
    data = board_outline.main_statements
    for drawing in board_outline.main_statements:
        if drawing.type == "APERTURE" and drawing.d == 10:
            delete_start = data.index(drawing)
        elif drawing.type == "APERTURE" and drawing.d != 10 and delete_start != -1:
            delete_end = data.index(drawing)
            break

    del data[delete_start:delete_end]


def add_layer(context, file_path, x, y, rotate):
    layer = gerberex.read(file_path)
    layer.to_metric()

    # if rotate:
    #    layer.rotate(90)

    layer.offset(x, y)
    context.merge(layer)


def place_top_fiducial(x, y):
    # Copper fiducial
    fiducial = gerberex.read(ELEMENTS_DIR + "fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    engrave_top_layer_context.merge(fiducial)


def place_bot_fiducial(x, y):
    # Copper fiducial
    fiducial = gerberex.read(ELEMENTS_DIR + "fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    engrave_bot_layer_context.merge(fiducial)


def add_pcb_top(pcb_name, x, y, rotate=False, generate_frame=True, merge_outline=True):
    pcb_file_path = INPUT_DIR + pcb_name + "/" + pcb_name
    board_outline_file_path = pcb_file_path + '.boardoutline.ger'
    board_outline = gerberex.read(board_outline_file_path)
    board_outline.to_metric()

    # Reset the board offset, set the bottom-left point of the board to 0, 0
    board_offset_x = board_outline.bounds[0][0]
    board_offset_y = board_outline.bounds[1][0]

    board_width = board_outline.size[0]
    board_height = board_outline.size[1]
    board_pos_x = x + frame_width + cutout_width
    board_pos_y = y + frame_width + cutout_width
    if generate_frame:
        generate_pcb_frame(board_cutout_msp, board_pos_x, board_pos_y, board_width, board_height, cutout_width)

    board_pos_x -= board_offset_x
    board_pos_y -= board_offset_y

    remove_gerber_outline(board_outline)

    board_outline.offset(board_pos_x, board_pos_y)
    if merge_outline:
        board_outline_context.merge(board_outline)

    add_layer(cream_top_layer_context, pcb_file_path + ".topcream.ger", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])


def add_pcb_bottom(pcb_name, x, y, rotate=False, generate_frame=True, merge_outline=True):
    pcb_file_path = INPUT_DIR + pcb_name + "/" + pcb_name
    board_outline_file_path = pcb_file_path + '.boardoutline-mirrored.ger'
    board_outline = gerberex.read(board_outline_file_path)
    board_outline.to_metric()

    # Reset the board offset, set the bottom-left point of the board to 0, 0
    board_offset_x = board_outline.bounds[0][0]
    board_offset_y = board_outline.bounds[1][0]

    board_width = board_outline.size[0]
    board_height = board_outline.size[1]
    board_pos_x = x + frame_width + cutout_width
    board_pos_y = y + frame_width + cutout_width
    if generate_frame:
        generate_pcb_frame(board_cutout_msp, board_pos_x, board_pos_y, board_width, board_height, cutout_width)

    board_pos_x -= board_offset_x
    board_pos_y -= board_offset_y

    remove_gerber_outline(board_outline)

    board_outline.offset(board_pos_x, board_pos_y)
    if merge_outline:
        board_outline_context.merge(board_outline)

    add_layer(cream_bot_layer_context, pcb_file_path + ".bottomcream-mirrored.ger", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])



def main():
    start_time = time.time()

    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76

    add_pcb_top("axiom_beta_sensor_cmv12000_tht_v0.16_r1.8c", 0, 0)
    add_pcb_top("axiom_beta_interface_dummy_v0.13_r1.6", 57.15 + cutout_width, 0)
    add_pcb_top("axiom_beta_main_board_v0.38_r1.2", 0, 57.15 + cutout_width)
    add_pcb_top("axiom_beta_power_board_v0.38_r1.2b", 57.15 + cutout_width, 57.15 + cutout_width)

    add_pcb_bottom("axiom_beta_sensor_cmv12000_tht_v0.16_r1.8c", 57.15 + cutout_width, 0)
    add_pcb_bottom("axiom_beta_interface_dummy_v0.13_r1.6", 0, 0)
    add_pcb_bottom("axiom_beta_main_board_v0.38_r1.2", 57.15 + cutout_width, 57.15 + cutout_width)
    add_pcb_bottom("axiom_beta_power_board_v0.38_r1.2b", 0, 57.15 + cutout_width)

    # fiducials in extra engrave layer
    place_top_fiducial(5, 2.5)
    #place_top_fiducial(5, panel_height - 2.5)
    place_top_fiducial(panel_width - 5, panel_height - 2.5)
    place_bot_fiducial(panel_width - 5, 2.5)
    place_bot_fiducial(5, panel_height - 2.5)
    #place_bot_fiducial(panel_width - 5, panel_height - 2.5)

    area = [0, 0, panel_width, panel_height]

    cream_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.topcream.ger")
    cream_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomcream.ger")
    engrave_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.topengrave.ger")
    engrave_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomengrave.ger")

    print(tabulate(pcb_info, headers=['Name', 'X', 'Y', 'Width', 'Height', 'Offset X', 'Offset Y'],
                   tablefmt='orgtbl'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

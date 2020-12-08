import os
import time
import sys
sys.path.append("..")

import ezdxf
import gerberex
from gerberex import DrillComposition
from gerberex import GerberComposition
from tabulate import tabulate

from frame_generator import generate_pcb_frame, generate_pcb_bridges, generate_outer_frame

ELEMENTS_DIR = "../input/elements/"
INPUT_DIR = "gerber_export/"
OUTPUT_DIR = "output_stage1/"
TEMP_DIR = "temp/"

cutout_width = 2.54  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()


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


board_outline_context = GerberComposition(settings=GerberSettings)
copper_layer_top_context = GerberComposition(settings=GerberSettings)
copper_layer_bot_context = GerberComposition(settings=GerberSettings)


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


def add_drill_layer(context, file_path, x, y, rotate):
    layer = gerberex.read(file_path, format=(2, 4))
    layer.to_metric()

    # if rotate:
    #    layer.rotate(90)

    layer.offset(x, y)
    context.merge(layer)


def add_pcb(pcb_name, x, y, rotate=False, generate_frame=True, merge_outline=True):
    pcb_file_path = INPUT_DIR + pcb_name + "/" + pcb_name
    board_outline_file_path = pcb_file_path + '.boardoutline.ger'
    board_outline = gerberex.read(board_outline_file_path)
    board_outline.to_metric()
    # if rotate:
    #    board_outline.rotate(90)

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

    add_layer(copper_layer_top_context, pcb_file_path + ".toplayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(copper_layer_bot_context, pcb_file_path + ".bottomlayer.ger", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])


def main():
    start_time = time.time()

    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76

    # Commented out to disable outer frame for mixed panel (stage 2)
    generate_outer_frame(board_cutout_msp, panel_width, panel_height)

    add_pcb("axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c_impedance", 0, 0)
    add_pcb("axiom_beta_interface_dummy_v0.13_r1.4_impedance", 57.15 + cutout_width, 0)
    add_pcb("axiom_beta_main_board_v0.37_r1.2_impedance", 0, 57.15 + cutout_width)
    add_pcb("axiom_beta_power_board_v0.37_r1.3_impedance", 57.15 + cutout_width, 57.15 + cutout_width)

    # impedance test strip
    add_pcb("test_strip_v0.1_r1.2_impedance", 0.1, 0.1, generate_frame=False, merge_outline=False)

    area = [0, 0, panel_width, panel_height]
    #generate_pcb_bridges(board_cutout_msp, area, cutout_width, 4, 6)

    board_cutout_doc.saveas(TEMP_DIR + 'board_outline.dxf')
    dxf_file = gerberex.read(TEMP_DIR + 'board_outline.dxf')
    board_outline_context.merge(dxf_file)
    board_outline_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.boardoutline.ger")

    copper_layer_top_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.toplayer.ger")
    copper_layer_bot_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomlayer.ger")


    print(tabulate(pcb_info, headers=['Name', 'X', 'Y', 'Width', 'Height', 'Offset X', 'Offset Y'],
                   tablefmt='orgtbl'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

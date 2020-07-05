import os

import ezdxf
import gerberex
from gerberex import GerberComposition
from tabulate import tabulate

from frame_generator import generate_outer_frame, generate_pcb_frame, generate_pcb_bridges

TEMPLATE_DIR = "templates/"
INPUT_DIR = "input/"
OUTPUT_DIR = "output/"

cutout_width = 2.5  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()

board_outline_context = GerberComposition()
copper_layer_top_context = GerberComposition()
soldermask_top_layer_context = GerberComposition()
silkscreen_top_layer_context = GerberComposition()
copper_layer_bot_context = GerberComposition()
soldermask_bot_layer_context = GerberComposition()
silkscreen_bot_layer_context = GerberComposition()
cream_top_layer_context = GerberComposition()
cream_bot_layer_context = GerberComposition()
internalplane1_layer_context = GerberComposition()
internalplane2_layer_context = GerberComposition()

def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


pcb_info = []


def add_layer(context, file_path, x, y, rotate):
    layer = gerberex.read(file_path)
    layer.to_metric()

    if rotate:
        layer.rotate(90)
    layer.offset(x, y)
    context.merge(layer)


def add_pcb(pcb_name, x, y, rotate=False):
    pcb_file_path = INPUT_DIR + pcb_name + "/" + pcb_name
    board_outline_file_path = pcb_file_path + '.boardoutline.ger'
    board_outline = gerberex.read(board_outline_file_path)
    board_outline.to_metric()
    if rotate:
        board_outline.rotate(90)

    # Reset the board offset, set the bottom-left point of the board to 0, 0
    board_offset_x = board_outline.bounds[0][0]
    board_offset_y = board_outline.bounds[1][0]

    board_width = board_outline.size[0]
    board_height = board_outline.size[1]
    board_pos_x = x + frame_width + cutout_width
    board_pos_y = y + frame_width + cutout_width
    generate_pcb_frame(board_cutout_msp, board_pos_x, board_pos_y, board_width, board_height, cutout_width)

    board_pos_x -= board_offset_x
    board_pos_y -= board_offset_y

    board_outline.offset(board_pos_x, board_pos_y)
    board_outline_context.merge(board_outline)

    add_layer(copper_layer_top_context, pcb_file_path + ".toplayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(soldermask_top_layer_context, pcb_file_path + ".topsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(silkscreen_top_layer_context, pcb_file_path + ".topsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(copper_layer_bot_context, pcb_file_path + ".bottomlayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(soldermask_bot_layer_context, pcb_file_path + ".bottomsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(silkscreen_bot_layer_context, pcb_file_path + ".bottomsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(cream_top_layer_context, pcb_file_path + ".tcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(cream_bot_layer_context, pcb_file_path + ".bcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(internalplane1_layer_context, pcb_file_path + ".internalplane1.ger", board_pos_x, board_pos_y, rotate)
    add_layer(internalplane2_layer_context, pcb_file_path + ".internalplane2.ger", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])

    # generate_pcb_frame(board_cutout_msp, board_pos_x, board_pos_y, board_width, board_height, cutout_width)


def place_panel_label(x, y):
    # silk screen label
    label = gerberex.read(INPUT_DIR + "elements/panel_label.gbr")
    label.to_metric()
    label.offset(x, y)
    silkscreen_top_layer_context.merge(label)

def place_subpanel_label(x, y):
    # silk screen label
    label = gerberex.read(INPUT_DIR + "elements/subpanel_label.gbr")
    label.to_metric()
    label.rotate(90)
    label.offset(x, y)
    silkscreen_top_layer_context.merge(label)

def place_top_fiducial(x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/fiducial_2.30mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    soldermask_top_layer_context.merge(fiducial)

    # Copper fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    copper_layer_top_context.merge(fiducial)

def place_top_origin(x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/origin_1.12mm_dia_circle_soldermask.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    soldermask_top_layer_context.merge(fiducial)

    # Copper cross
    fiducial = gerberex.read(INPUT_DIR + "elements/origin_cross.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    copper_layer_top_context.merge(fiducial)

def place_bot_fiducial(x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/fiducial_2.30mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    soldermask_bot_layer_context.merge(fiducial)

    # Copper fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    copper_layer_bot_context.merge(fiducial)

def place_bot_origin(x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(INPUT_DIR + "elements/origin_1.12mm_dia_circle_soldermask.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    soldermask_bot_layer_context.merge(fiducial)

    # Copper cross
    fiducial = gerberex.read(INPUT_DIR + "elements/origin_cross.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    copper_layer_bot_context.merge(fiducial)

def main():
    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76;
    generate_outer_frame(board_cutout_msp, panel_width, panel_height)

    add_pcb("axiom_beta_sensor_cmv12000_tht_v0.16_r1.3", 0, 0)
    add_pcb("axiom_beta_interface_dummy_v0.13_r1.1", 57.15 + cutout_width,
            0)
    add_pcb("axiom_beta_main_board_v0.36_r1.2", 0, 57.15 + cutout_width, True)
    add_pcb("axiom_beta_power_board_v0.30", 57.15 + cutout_width, 57.15 + cutout_width, True)

    area = [0, 0, panel_width, panel_height]
    generate_pcb_bridges(board_cutout_msp, area, cutout_width, 4, 6)

    #fiducials
    place_top_fiducial(2.5, 2.5)
    place_top_fiducial(2.5, panel_height - 2.5)
    place_top_fiducial(panel_width - 2.5, panel_height - 2.5)
    place_bot_fiducial(2.5, 2.5)
    place_bot_fiducial(2.5, panel_height - 2.5)
    place_bot_fiducial(panel_width - 2.5, panel_height - 2.5)

    #origin
    place_top_origin(panel_width - 2.5, 2.5)
    place_bot_origin(panel_width - 2.5, 2.5)

    #labels
    place_subpanel_label(panel_width-1.5, 8)

    board_cutout_doc.saveas(OUTPUT_DIR + 'board_outline.dxf')
    dxf_file = gerberex.read(OUTPUT_DIR + 'board_outline.dxf')
    # dxf_file.draw_mode = dxf_file.DM_FILL
    board_outline_context.merge(dxf_file)
    board_outline_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.boardoutline.ger")

    copper_layer_top_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.toplayer.ger")
    soldermask_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.topsoldermask.ger")
    silkscreen_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.topsilkscreen.ger")
    copper_layer_bot_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomlayer.ger")
    soldermask_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomsoldermask.ger")
    silkscreen_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bottomsilkscreen.ger")
    cream_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.tcream.ger")
    cream_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.bream.ger")
    internalplane1_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.internalplane1.ger")
    internalplane2_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.internalplane2.ger")

    print(tabulate(pcb_info, headers=['Name', 'X', 'Y', 'Width', 'Height', 'Offset X', 'Offset Y'], tablefmt='orgtbl'))


if __name__ == "__main__":
    # execute only if run as a script
    main()

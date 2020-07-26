import ezdxf
import gerberex
import os
from gerberex import DrillComposition
from gerberex import GerberComposition
from tabulate import tabulate

from frame_generator import generate_outer_frame, generate_pcb_frame

TEMPLATE_DIR = "templates/"
INPUT_DIR = "output_stage1/"
OUTPUT_DIR = "output_stage2/"

cutout_width = 2.5  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()


class GerberSettings:
    format = [3, 6]
    units = "metric"
    zero_suppression = "trailing"


class DrillSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


board_outline_context = GerberComposition(settings=GerberSettings)
copper_layer_top_context = GerberComposition(settings=GerberSettings)
soldermask_top_layer_context = GerberComposition(settings=GerberSettings)
silkscreen_top_layer_context = GerberComposition(settings=GerberSettings)
copper_layer_bot_context = GerberComposition(settings=GerberSettings)
soldermask_bot_layer_context = GerberComposition(settings=GerberSettings)
silkscreen_bot_layer_context = GerberComposition(settings=GerberSettings)
cream_top_layer_context = GerberComposition(settings=GerberSettings)
cream_bot_layer_context = GerberComposition(settings=GerberSettings)
internalplane1_layer_context = GerberComposition(settings=GerberSettings)
internalplane2_layer_context = GerberComposition(settings=GerberSettings)

drills_context = DrillComposition(settings=DrillSettings)


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
    pcb_file_path = INPUT_DIR + "/" + pcb_name
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

    '''add_layer(copper_layer_top_context, pcb_file_path + ".toplayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(soldermask_top_layer_context, pcb_file_path + ".topsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(silkscreen_top_layer_context, pcb_file_path + ".topsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(copper_layer_bot_context, pcb_file_path + ".bottomlayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(soldermask_bot_layer_context, pcb_file_path + ".bottomsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(silkscreen_bot_layer_context, pcb_file_path + ".bottomsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(cream_top_layer_context, pcb_file_path + ".topcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(cream_bot_layer_context, pcb_file_path + ".bottomcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(internalplane1_layer_context, pcb_file_path + ".internalplane1.ger", board_pos_x, board_pos_y, rotate)
    add_layer(internalplane2_layer_context, pcb_file_path + ".internalplane2.ger", board_pos_x, board_pos_y, rotate)'''

    add_layer(drills_context, pcb_file_path + ".drills.xln", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])

    # generate_pcb_frame(board_cutout_msp, board_pos_x, board_pos_y, board_width, board_height, cutout_width)


def place_panel_label(x, y):
    # silk screen label
    label = gerberex.read("input/elements/panel_label.gbr")
    label.to_metric()
    label.offset(x, y)
    silkscreen_top_layer_context.merge(label)


def main():
    setup()

    panel_width = 550
    panel_height = 580
    generate_outer_frame(board_cutout_msp, panel_width, panel_height)

    # row 1
    add_pcb("axiom_beta_mixed_panel", 0 + 5, 0 + 5)
    add_pcb("axiom_beta_mixed_panel", 134.3 + 5, 0 + 5)
    add_pcb("axiom_beta_mixed_panel", 268.6 + 5, 0 + 5)
    add_pcb("axiom_beta_mixed_panel", 402.9 + 5, 0 + 5)

    # row 2
    add_pcb("axiom_beta_mixed_panel", 0 + 5, 188.91 + 5)
    add_pcb("axiom_beta_mixed_panel", 134.3 + 5, 188.91 + 5)
    add_pcb("axiom_beta_mixed_panel", 268.6 + 5, 188.91 + 5)
    add_pcb("axiom_beta_mixed_panel", 402.9 + 5, 188.91 + 5)

    # row 3
    add_pcb("axiom_beta_mixed_panel", 0 + 5, 377.82 + 5)
    add_pcb("axiom_beta_mixed_panel", 134.3 + 5, 377.82 + 5)
    add_pcb("axiom_beta_mixed_panel", 268.6 + 5, 377.82 + 5)
    add_pcb("axiom_beta_mixed_panel", 402.9 + 5, 377.82 + 5)

    # area = [0, 0, panel_width, panel_height]
    # generate_pcb_bridges(board_cutout_msp, area, cutout_width, 4, 6)

    # label
    place_panel_label(3, 1.5)

    board_cutout_doc.saveas(OUTPUT_DIR + 'board_outline.dxf')
    dxf_file = gerberex.read(OUTPUT_DIR + 'board_outline.dxf')
    # dxf_file.draw_mode = dxf_file.DM_FILL
    board_outline_context.merge(dxf_file)
    board_outline_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.boardoutline.ger")

    '''copper_layer_top_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.toplayer.ger")
    soldermask_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.topsoldermask.ger")
    silkscreen_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.topsilkscreen.ger")
    copper_layer_bot_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.bottomlayer.ger")
    soldermask_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.bottomsoldermask.ger")
    silkscreen_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.bottomsilkscreen.ger")
    cream_top_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.topcream.ger")
    cream_bot_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.bottomcream.ger")
    internalplane1_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.internalplane1.ger")
    internalplane2_layer_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.internalplane2.ger")'''

    drills_context.dump(OUTPUT_DIR + "axiom_beta_mixed_multi_panel.drills.xln")

    print(tabulate(pcb_info, headers=['Name', 'X', 'Y', 'Width', 'Height', 'Offset X', 'Offset Y'], tablefmt='orgtbl'))


if __name__ == "__main__":
    # execute only if run as a script
    main()

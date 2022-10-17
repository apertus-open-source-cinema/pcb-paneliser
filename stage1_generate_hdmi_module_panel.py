import os
import time

import ezdxf
import gerberex
from tabulate import tabulate

import pcb_panel_config as cfg
from frame_generator import generate_pcb_frame, generate_pcb_bridges, generate_outer_frame
from pcb_scripts import pcb_draw_helpers
from pcb_scripts import pcb_helpers
from pcb_scripts.pcb_panel_info import PCBPanel

cutout_width = 2.54  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()

board_info_doc = ezdxf.new('R2010')
board_info_msp = board_info_doc.modelspace()

'''board_outline = GerberComposition(settings=GerberSettings)
copper_layer_top = GerberComposition(settings=GerberSettings)
soldermask_top_layer = GerberComposition(settings=GerberSettings)
silkscreen_top_layer = GerberComposition(settings=GerberSettings)
copper_layer_bot = GerberComposition(settings=GerberSettings)
soldermask_bot_layer = GerberComposition(settings=GerberSettings)
silkscreen_bot_layer = GerberComposition(settings=GerberSettings)
cream_top_layer = GerberComposition(settings=GerberSettings)
cream_bot_layer = GerberComposition(settings=GerberSettings)
internalplane1_layer = GerberComposition(settings=GerberSettings)
internalplane2_layer = GerberComposition(settings=GerberSettings)

drills = DrillComposition(settings=DrillSettings)'''

pcb_panel = PCBPanel()
pcb_info = []


def setup():
    if not os.path.exists(cfg.OUTPUT_DIR):
        os.makedirs(cfg.OUTPUT_DIR)
    if not os.path.exists(cfg.TEMP_DIR):
        os.makedirs(cfg.TEMP_DIR)


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
    pcb_file_path = cfg.INPUT_DIR + pcb_name + "/" + pcb_name
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

    pcb_helpers.remove_gerber_outline(board_outline)

    board_outline.offset(board_pos_x, board_pos_y)
    if merge_outline:
        pcb_panel.board_outline.merge(board_outline)

    add_layer(pcb_panel.copper_layer_top, pcb_file_path + ".toplayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.soldermask_top_layer, pcb_file_path + ".topsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.silkscreen_top_layer, pcb_file_path + ".topsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.copper_layer_bot, pcb_file_path + ".bottomlayer.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.soldermask_bot_layer, pcb_file_path + ".bottomsoldermask.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.silkscreen_bot_layer, pcb_file_path + ".bottomsilkscreen.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.cream_top_layer, pcb_file_path + ".topcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.cream_bot_layer, pcb_file_path + ".bottomcream.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.internalplane1_layer, pcb_file_path + ".internalplane1.ger", board_pos_x, board_pos_y, rotate)
    add_layer(pcb_panel.internalplane2_layer, pcb_file_path + ".internalplane2.ger", board_pos_x, board_pos_y, rotate)

    add_drill_layer(pcb_panel.drills, pcb_file_path + ".drills.xln", board_pos_x, board_pos_y, rotate)

    pcb_info.append([pcb_name, x, y, board_width, board_height, board_offset_x, board_offset_y])


def save_pcb_layers():
    pcb_panel.copper_layer_top.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.toplayer.ger")
    pcb_panel.soldermask_top_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.topsoldermask.ger")
    pcb_panel.silkscreen_top_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.topsilkscreen.ger")
    pcb_panel.copper_layer_bot.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.bottomlayer.ger")
    pcb_panel.soldermask_bot_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.bottomsoldermask.ger")
    pcb_panel.silkscreen_bot_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.bottomsilkscreen.ger")
    pcb_panel.cream_top_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.topcream.ger")
    pcb_panel.cream_bot_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.bottomcream.ger")
    pcb_panel.internalplane1_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.internalplane1.ger")
    pcb_panel.internalplane2_layer.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.internalplane2.ger")
    pcb_panel.drills.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.drills.xln")


def main():
    start_time = time.time()

    setup()

    panel_width = frame_width * 2 + cutout_width * 4 + 30.625 * 3
    panel_height = frame_width * 2 + cutout_width * 4 + 28.321 * 3

    # Commented out to disable outer frame for mixed panel (stage 2)
    generate_outer_frame(board_cutout_msp, panel_width, panel_height)

    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 0, 0)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 30.625 + cutout_width, 0)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", (30.625 + cutout_width) * 2, 0)

    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 0, 28.321 + cutout_width)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 30.625 + cutout_width, 28.321 + cutout_width)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", (30.625 + cutout_width) * 2, 28.321 + cutout_width)

    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 0, (28.321 + cutout_width) * 2)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", 30.625 + cutout_width, (28.321 + cutout_width) * 2)
    add_pcb("axiom_beta_hdmi_plugin_module_v0.8_r1.2", (30.625 + cutout_width) * 2, (28.321 + cutout_width) * 2)

    # add_pcb("axiom_beta_interface_dummy_v0.13_r1.6", 57.15 + cutout_width, 0)
    # add_pcb("axiom_beta_main_board_v0.38_r1.2", 0, 57.15 + cutout_width)
    # add_pcb("axiom_beta_power_board_v0.38_r1.2", 57.15 + cutout_width, 57.15 + cutout_width)

    # impedance test strip
    # add_pcb("test_strip_v0.1_r1.2", 0.1, 0.1, generate_frame=False, merge_outline=False)

    area = [0, 0, panel_width, panel_height]
    generate_pcb_bridges(board_cutout_msp, area, cutout_width, 4, 6)

    # fiducials
    pcb_draw_helpers.place_top_fiducial(pcb_panel, 5, 2.5)
    pcb_draw_helpers.place_top_fiducial(pcb_panel, 5, panel_height - 2.5)
    pcb_draw_helpers.place_top_fiducial(pcb_panel, panel_width - 5, panel_height - 2.5)
    pcb_draw_helpers.place_bot_fiducial(pcb_panel, 5, 2.5)
    pcb_draw_helpers.place_bot_fiducial(pcb_panel, 5, panel_height - 2.5)
    pcb_draw_helpers.place_bot_fiducial(pcb_panel, panel_width - 5, panel_height - 2.5)

    # origin
    pcb_draw_helpers.place_top_origin(pcb_panel, panel_width - 5, 2.5)
    pcb_draw_helpers.place_bot_origin(pcb_panel, panel_width - 5, 2.5)

    # labels
    pcb_draw_helpers.place_subpanel_label(board_info_msp, "AXIOM Beta 9x HDMI Plugin Module Panel V0.1", 3.5, 8)

    board_cutout_doc.saveas(cfg.TEMP_DIR + 'board_outline.dxf')
    dxf_file = gerberex.read(cfg.TEMP_DIR + 'board_outline.dxf')
    pcb_panel.board_outline.merge(dxf_file)
    pcb_panel.board_outline.dump(cfg.OUTPUT_DIR + "axiom_beta_mixed_panel.boardoutline.ger")

    board_info_doc.saveas(cfg.TEMP_DIR + 'board_info.dxf')
    dxf_file = gerberex.read(cfg.TEMP_DIR + 'board_info.dxf')
    dxf_file.width = 0.2
    pcb_panel.silkscreen_top_layer.merge(dxf_file)

    save_pcb_layers()

    print(tabulate(pcb_info, headers=['Name', 'X', 'Y', 'Width', 'Height', 'Offset X', 'Offset Y'],
                   tablefmt='orgtbl'))

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

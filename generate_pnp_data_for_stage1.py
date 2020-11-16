import os
import time
from math import radians
from xml.etree import ElementTree

import ezdxf
import gerberex
from gerberex import GerberComposition

INPUT_DIR = "input/base_variant/"
OUTPUT_DIR = "output_stage1_pnp/"
EAGLE_DATA_DIR = "input/EAGLE/"
TEMP_DIR = "temp/"

components_top = []
components_bottom = []

components_top_doc = ezdxf.new('R2010')
components_top_msp = components_top_doc.modelspace()

components_bottom_doc = ezdxf.new('R2010')
components_bottom_msp = components_bottom_doc.modelspace()


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


component_context_top = GerberComposition(settings=GerberSettings)
component_context_bottom = GerberComposition(settings=GerberSettings)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def get_board_dimensions(xml_root):
    dimensions = xml_root.findall(".//wire[@layer=\"20\"]")

    min_x = 0.0
    min_y = 0.0
    max_x = 0.0
    max_y = 0.0

    for dimension in dimensions:
        if float(dimension.attrib["x1"]) < min_x:
            min_x = float(dimension.attrib["x1"])
        if float(dimension.attrib["y1"]) < min_y:
            min_y = float(dimension.attrib["y1"])
        if float(dimension.attrib["x2"]) > max_x:
            max_x = float(dimension.attrib["x2"])
        if float(dimension.attrib["y2"]) > max_y:
            max_y = float(dimension.attrib["y2"])

    offset_x = abs(max_x) - abs(min_x)
    offset_y = abs(max_y) - abs(min_y)

    return min_x, min_y, max_x - min_x, max_y - min_y, abs(offset_x), abs(offset_y)


def get_components(pcb_name, suffix, offset_x, offset_y, rotated=False):
    brd_path = EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".brd"
    tree = ElementTree.parse(brd_path)
    xml_root = tree.getroot()
    board_x, board_y, board_width, board_height, board_offset_x, board_offset_y = get_board_dimensions(xml_root)

    if rotated:
        board_width, board_height = board_height, board_width
        board_offset_x, board_offset_y = board_offset_y, board_offset_x

    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnt", "r")
    for line in file:
        name, x, y, rotation, *temp = line.split()
        if rotated:
            x, y = -float(y), x
            rotation = int(rotation) + 90

        x = float(x) + offset_x + board_width / 2 + board_offset_x / 2
        y = float(
                y) + offset_y + board_height / 2 + board_offset_y / 2
        components_top.append((name + suffix, x, y, int(rotation) % 360))

    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnb", "r")
    for line in file:
        name, x, y, rotation, *temp = line.split()
        if rotated:
            x, y = -float(y), x
            rotation = int(rotation) + 180

        x = float(x) + offset_x + board_width / 2 + board_offset_x / 2
        y = float(
                y) + offset_y + board_height / 2 + board_offset_y / 2
        components_bottom.append((name + suffix, x, y, int(rotation) % 360))


def draw_component_positions():
    for element in components_top:
        name, x, y, rotation, *temp = element
        components_top_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.3)], format="xy").rotate_z(
                radians(int(rotation))).translate(x, y, 0)
        components_top_msp.add_circle((x, y), 0.2)

    for element in components_bottom:
        name, x, y, rotation, *temp = element
        components_bottom_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.3)], format="xy").rotate_z(
                radians(int(rotation))).translate(x, y, 0)
        components_bottom_msp.add_circle((x, y), 0.2)


def write_origin(file_top, file_bottom):
    file_top.write("2,5|2,5|0|0\n\n")
    file_bottom.write("2,5|2,5|0|0\n\n")


def write_component_positions(file_top, file_bottom):
    for component in components_top:
        name, x, y, rotation = component
        file_top.write(
            name + "|" + str(x).replace(".", ",") + "|" + str(y).replace(".", ",") + "|" + str(rotation).replace(".",
                                                                                                                 ",") + "\n")

    for component in components_bottom:
        name, x, y, rotation = component
        file_bottom.write(
            name + "|" + str(x).replace(".", ",") + "|" + str(y).replace(".", ",") + "|" + str(rotation).replace(".",
                                                                                                                 ",") + "\n")


def generate_background(suffix, cream_layer_file):
    board_context = GerberComposition(settings=GerberSettings)
    cream_layer = gerberex.read(cream_layer_file)
    board_context.merge(cream_layer)
    board_outline = gerberex.read('output_stage1/WITH_OUTLINE_axiom_beta_mixed_panel.boardoutline.ger')
    board_context.merge(board_outline)
    board_context.dump(OUTPUT_DIR + "pnp_background_" + suffix + ".ger")


def main():
    start_time = time.time()

    if not os.path.exists(OUTPUT_DIR + "pnp_background_top.ger"):
        generate_background('top', 'output_stage1/axiom_beta_mixed_panel.topcream.ger')

    if not os.path.exists(OUTPUT_DIR + "pnp_background_bottom.ger"):
        generate_background('bottom', 'output_stage1/axiom_beta_mixed_panel.bottomcream.ger')

    get_components("axiom_beta_main_board_v0.37_r1.1", "_1", 7.5, 10 + 57.15, True)  # 7.5 + 57.15
    get_components("axiom_beta_power_board_v0.37_r1.2", "_2", 57.15 + 10, 57.15 + 10, True)
    get_components("axiom_beta_interface_dummy_v0.13_r1.3", "_3", 10 + 57.15, 7.5)
    get_components("axiom_beta_sensor_cmv12000_tht_v0.16_r1.5c", "_4", 7.5, 7.5)

    draw_component_positions()

    components_top_doc.saveas(TEMP_DIR + "components_top.dxf")
    dxf = gerberex.read(TEMP_DIR + "components_top.dxf")
    component_context_top.merge(dxf)
    component_context_top.dump(OUTPUT_DIR + "component_position_top.ger")

    components_bottom_doc.saveas(TEMP_DIR + "components_bottom.dxf")
    dxf = gerberex.read(TEMP_DIR + "components_bottom.dxf")
    component_context_bottom.merge(dxf)
    component_context_bottom.dump(OUTPUT_DIR + "component_position_bottom.ger")

    file_top = open(OUTPUT_DIR + "pnp_data_top.asc", "w")
    file_bottom = open(OUTPUT_DIR + "pnp_data_bottom.asc", "w")

    write_origin(file_top, file_bottom)
    write_component_positions(file_top, file_bottom)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

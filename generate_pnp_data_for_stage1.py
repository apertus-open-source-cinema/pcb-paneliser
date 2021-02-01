# IMPORTANT: Ensure that the export of .mnt and .mnb files from EAGLE  was done for "Tele" variant
import csv
import os
import time
from math import radians
from xml.etree import ElementTree

import ezdxf
import gerberex
from HersheyFonts import HersheyFonts
from gerberex import GerberComposition
from tabulate import tabulate

INPUT_DIR = "input/tele_variant/"
OUTPUT_DIR = "output_stage1_pnp/"
EAGLE_DATA_DIR = "input/EAGLE/"
TEMP_DIR = "temp/"

BOM_FILE = "input/BOM/BOM_old.tsv"

ORIGIN_OFFSET_X = 5
ORIGIN_OFFSET_Y = 2.5

component_summary = []
components_top = []
components_bottom = []
tele_components = {}

components_top_doc = ezdxf.new('R2010')
components_top_msp = components_top_doc.modelspace()

components_bottom_doc = ezdxf.new('R2010')
components_bottom_msp = components_bottom_doc.modelspace()

font = HersheyFonts()
font.load_default_font()


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


component_context_top = GerberComposition(settings=GerberSettings)
component_context_bottom = GerberComposition(settings=GerberSettings)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)


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


def draw_text(text, x, y):
    for (x1, y1), (x2, y2) in font.lines_for_text(text):
        x1, y1, x2, y2 = x1 + x, y1 + y, x2 + x, y2 + y

        components_top_msp.add_lwpolyline([(x1, y1), (x2, y2)],
                                          format='xy')


def get_components(pcb_name, suffix, offset_x, offset_y, rotated=False):
    components_top_count = len(components_top)
    components_bottom_count = len(components_bottom)
    brd_path = EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".brd"
    tree = ElementTree.parse(brd_path)
    xml_root = tree.getroot()
    board_x, board_y, board_width, board_height, board_offset_x, board_offset_y = get_board_dimensions(xml_root)

    if rotated:
        board_width, board_height = board_height, board_width
        board_offset_x, board_offset_y = board_offset_y, board_offset_x

    pcb_file_name = EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnt"
    file = open(pcb_file_name, "r")
    for line in file:
        name, x, y, rotation, *temp = line.split()
        if rotated:
            x, y = -float(y), x
            rotation = int(rotation) + 90

        x = float(x) + offset_x + board_width / 2.0 + board_offset_x / 2.0
        y = float(
                y) + offset_y + board_height / 2.0 + board_offset_y / 2.0
        x, y = x - ORIGIN_OFFSET_X, y - ORIGIN_OFFSET_Y
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
        x, y = x - ORIGIN_OFFSET_X, y - ORIGIN_OFFSET_Y
        components_bottom.append((name + suffix, x, y, int(rotation) % 360))
    component_summary.append(
            [pcb_name, len(components_top) - components_top_count, len(components_bottom) - components_bottom_count])
    # print("{}: {} top components / {} bottom components".format(pcb_name, len(components_top), len(components_bottom)))

    '''def draw_component_positions():
        for element in components_top:
            name, x, y, rotation, *temp = element
            components_top_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.3)], format="xy").rotate_z(
                    radians(int(rotation))).translate(x, y, 0)
            components_top_msp.add_circle((x, y), 0.2)
    
        for element in components_bottom:
            name, x, y, rotation, *temp = element
            components_bottom_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.3)], format="xy").rotate_z(
                    radians(int(rotation))).translate(x, y, 0)
            components_bottom_msp.add_circle((x, y), 0.2)'''


def draw_component_positions():
    global components_top, components_bottom
    components_top = []
    components_bottom = []

    # Draw origin
    components_top_msp.add_circle((ORIGIN_OFFSET_X, ORIGIN_OFFSET_Y), 0.2)
    components_top_msp.add_circle((ORIGIN_OFFSET_X, ORIGIN_OFFSET_Y), 0.0)

    # Draw origin
    components_top_msp.add_circle((0.0, 0.0), 0.2)
    components_top_msp.add_circle((0.0, 0.0), 0.0)

    file_top = open(OUTPUT_DIR + "pnp_data_top.asc", "r")
    offset_x, offset_y, *temp = file_top.readline().replace(',', '.').split('|')
    file_top.readline()  # Skip empty line
    for entry in file_top:
        name, tele_id, x, y, rotation = entry.replace(',', '.').rstrip().split('|')
        components_top_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.5)], format="xy").rotate_z(
                radians(int(rotation))).translate(float(x) + float(offset_x), float(y) + float(offset_y), 0)
        components_top_msp.add_circle((float(x) + float(offset_x), float(y) + float(offset_y)), 0.2)
        font.normalize_rendering(0.5)
        # draw_text(name, float(x) + float(offset_x), float(y) + float(offset_y))
    file_bottom = open(OUTPUT_DIR + "pnp_data_bottom.asc", "r")


def write_origin(file_top, file_bottom):
    file_top.write("{}|{}|0|0\n\n".format(ORIGIN_OFFSET_X, str(ORIGIN_OFFSET_Y).replace('.', ',')))
    file_bottom.write("{}|{}|0|0\n\n".format(ORIGIN_OFFSET_X, str(ORIGIN_OFFSET_Y).replace('.', ',')))


def write_component_positions(file_top, file_bottom):
    for component in components_top:
        name, x, y, rotation = component
        tele_id = tele_components.get(name, "")
        file_top.write(
                "{}|{}|{}|{}|{}\n".format(name, tele_id, str(round(x, 4)).replace(".", ","),
                                          str(round(y, 4)).replace(".", ","), str(rotation).replace(".", ",")))

    for component in components_bottom:
        name, x, y, rotation = component
        tele_id = tele_components.get(name, "")
        file_bottom.write(
                "{}|{}|{}|{}|{}\n".format(name, tele_id, str(round(x, 4)).replace(".", ","),
                                          str(round(y, 4)).replace(".", ","), str(rotation).replace(".", ",")))


def generate_background(suffix, cream_layer_file):
    board_context = GerberComposition(settings=GerberSettings)
    cream_layer = gerberex.read(cream_layer_file)
    board_context.merge(cream_layer)
    board_outline = gerberex.read('output_stage1/axiom_beta_mixed_panel.boardoutline.ger')
    board_context.merge(board_outline)
    board_context.dump(OUTPUT_DIR + "pnp_background_" + suffix + ".ger")


def load_bom_components():
    with open(BOM_FILE) as bom_file:
        for i in range(4):
            next(bom_file)
        reader = csv.DictReader(bom_file, delimiter='\t')
        for row in reader:
            pcb_name = row["PCB"][:2]
            parts = row['Combined Sch. Reference (*.asc)'].split(',')
            tele_id = row["Tele ID"]
            for part in parts:
                part = part.strip()
                tele_components[part + "_" + pcb_name] = tele_id.strip()


def main():
    start_time = time.time()

    setup()

    if not os.path.exists(OUTPUT_DIR + "pnp_background_top.ger"):
        generate_background('top', 'output_stage1/axiom_beta_mixed_panel.topcream.ger')

    if not os.path.exists(OUTPUT_DIR + "pnp_background_bottom.ger"):
        generate_background('bottom', 'output_stage1/axiom_beta_mixed_panel.bottomcream.ger')

    get_components("axiom_beta_main_board_v0.38_r1.2", "_MB", 5 + 2.54, 5 + 2.54 * 2 + 57.15, True)  # 7.5 + 57.15
    get_components("axiom_beta_power_board_v0.38_r1.2b", "_PB", 57.15 + 5 + 2.54 * 2, 57.15 + 5 + 2.54 * 2, True)
    get_components("axiom_beta_interface_dummy_v0.13_r1.6", "_IB", 5 + 2.54 * 2 + 57.15, 5 + 2.54)
    get_components("axiom_beta_sensor_cmv12000_tht_v0.16_r1.8c", "_SB", 5 + 2.54, 5 + 2.54)

    print(tabulate(component_summary, headers=["Name", "Components (top)", "Components (bottom)"]))

    load_bom_components()

    file_top = open(OUTPUT_DIR + "pnp_data_top.asc", "w")
    file_bottom = open(OUTPUT_DIR + "pnp_data_bottom.asc", "w")

    write_origin(file_top, file_bottom)
    write_component_positions(file_top, file_bottom)

    file_top.flush()
    file_top.close()
    file_bottom.flush()
    file_bottom.close()

    draw_component_positions()
    components_top_doc.saveas(TEMP_DIR + "components_top.dxf")
    dxf = gerberex.read(TEMP_DIR + "components_top.dxf")
    dxf.width = 0.05
    component_context_top.merge(dxf)
    component_context_top.dump(OUTPUT_DIR + "component_position_top.ger")

    # components_bottom_doc.saveas(TEMP_DIR + "components_bottom.dxf")
    # dxf = gerberex.read(TEMP_DIR + "components_bottom.dxf")
    # component_context_bottom.merge(dxf)
    # component_context_bottom.dump(OUTPUT_DIR + "component_position_bottom.ger")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

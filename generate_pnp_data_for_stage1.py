# IMPORTANT: Ensure that the export of .mnt and .mnb files from EAGLE  was done for "Tele" variant

import csv
import math
import os
import time
from math import radians
from xml.etree import ElementTree

import drawSvg as draw
import gerberex
from PIL import Image
from tabulate import tabulate

INPUT_DIR = "input/pnp_background/"
OUTPUT_DIR = "output_stage1_pnp/"
EAGLE_DATA_DIR = "input/EAGLE/"
TEMP_DIR = "temp/"

BOM_FILE = "input/BOM/BOM.tsv"

ORIGIN_OFFSET_X = 2.5
ORIGIN_OFFSET_Y = 5

cutout_width = 2.54
frame_width = 5

component_summary = []
components_top = []
components_bottom = []
tele_components = {}

drawing_top = None
drawing_bottom = None
factor = 1.0

output_image_height = 0


def get_image_size(image_file_name):
    image = Image.open(image_file_name)
    return image.width, image.height


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    background_top = INPUT_DIR + "axiom_beta_mixed_panel.top_rotated.png"
    background_bottom = INPUT_DIR + "axiom_beta_mixed_panel.bottom_rotated.png"

    board_x = 0
    board_y = 0

    board_outline = gerberex.read('output_stage1/axiom_beta_mixed_panel.boardoutline.ger')

    board_width = board_outline.size[1]
    board_height = board_outline.size[0]

    image_width, image_height = get_image_size(background_top)

    global drawing_top, drawing_bottom, factor, output_image_height

    output_image_width = image_width / 2
    output_image_height = image_height / 2

    factor = (output_image_width / board_width + output_image_height / board_height) / 2

    # Fixed size for PCB image
    drawing_top = draw.Drawing(output_image_width, output_image_height)
    drawing_bottom = draw.Drawing(output_image_width, output_image_height)

    # Draw background
    drawing_top.append(draw.Image(board_x * factor, board_y * factor,
                                  output_image_width, output_image_height, background_top))

    drawing_top.append(draw.Rectangle(0, 0, output_image_width, output_image_height, fill="black", opacity=0.5))

    drawing_bottom.append(draw.Image(board_x * factor, board_y * factor,
                                     output_image_width, output_image_height, background_bottom))

    drawing_bottom.append(draw.Rectangle(0, 0, output_image_width, output_image_height, fill="black", opacity=0.5))


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


first_pads = {}
part_package = {}


def load_pad_data(xml_root, suffix):
    element_list = xml_root.findall(".//element")
    for item in element_list:
        element_name = item.attrib["name"] + suffix
        package_name = item.attrib["package"] + suffix
        part_package[element_name] = package_name

    package_list = xml_root.findall(".//package")
    for item in package_list:
        package_name = item.attrib["name"] + suffix

        smd_list = item.findall("smd")
        for smd in smd_list:
            name = smd.attrib["name"]
            if name != "1":
                continue

            x = smd.attrib['x']
            y = smd.attrib['y']
            first_pads[package_name] = (float(x), float(y))

        pad_list = item.findall("pad")
        for via in pad_list:
            name = via.attrib["name"]
            if name != "1":
                continue

            x = via.attrib['x']
            y = via.attrib['y']
            first_pads[package_name] = (float(x), float(y))


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
            x, y = y, -float(x)
            rotation = int(rotation) + 270

        x = float(x) + offset_x + board_width / 2.0 + board_offset_x / 2.0
        y = float(
                y) + offset_y + board_height / 2.0 + board_offset_y / 2.0
        x, y = x - ORIGIN_OFFSET_X, y - ORIGIN_OFFSET_Y
        components_top.append((name + suffix, x, y, int(rotation) % 360))

    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnb", "r")
    for line in file:
        name, x, y, rotation, *temp = line.split()
        if rotated:
            x, y = y, -float(x)
            rotation = int(rotation) + 90

        x = float(x) + offset_x + board_width / 2 + board_offset_x / 2.0
        y = float(
                y) + offset_y + board_height / 2 + board_offset_y / 2.0
        x, y = x - ORIGIN_OFFSET_X, y - ORIGIN_OFFSET_Y
        components_bottom.append((name + suffix, x, y, int(rotation) % 360))
    component_summary.append(
            [pcb_name, len(components_top) - components_top_count, len(components_bottom) - components_bottom_count])

    load_pad_data(xml_root, suffix)


def draw_component_positions(filename, drawing, bottom_layer=False):
    file = open(filename, 'r')
    offset_x, offset_y, *temp = file.readline().replace(',', '.').split('|')
    file.readline()  # Skip empty line
    for entry in file:
        name, tele_id, x, y, rotation = entry.replace(',', '.').rstrip().split('|')
        x = float(x) + float(offset_x)
        y = float(y) + float(offset_y)
        x = x * factor
        y = y * factor

        if bottom_layer:
            y = output_image_height - y
            rotation = int(rotation) + 180

        drawing.append(
                draw.Circle(x, y, 0.3 * factor, fill="yellow"))
        rotation_transform = str.format(
                "translate({1}, {2}) rotate({0}) ", str(-int(rotation)), str(x), str(-y))

        drawing.append(
                draw.Line(0, 0, 0, 1 * factor, stroke="red", stroke_width=2, transform=rotation_transform))

        if name in part_package:
            package = part_package[name]
            if package in first_pads:
                pad_position = first_pads[package]
                pad_x = pad_position[0] * factor
                pad_y = pad_position[1] * factor

                angle_rad = radians(int(rotation))
                rot_x = pad_x * math.cos(angle_rad) - pad_y * math.sin(angle_rad)
                rot_y = pad_x * math.sin(angle_rad) + pad_y * math.cos(angle_rad)

                rotation_transform = str.format(
                        "translate({1}, {2}) rotate({0})", str(-int(rotation)), str(x), str(-y))
                drawing.append(draw.Circle(pad_x, pad_y, 0.2 * factor, fill="blue", transform=rotation_transform))
                drawing.append(
                        draw.Text(name, 1 * factor, x - rot_x, y + rot_y, stroke="#444444", fill="lightgreen"))


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


def load_bom_components():
    with open(BOM_FILE) as bom_file:
        for i in range(4):
            next(bom_file)
        reader = csv.DictReader(bom_file, delimiter='\t')
        for row in reader:
            parts = row['Combined Sch. Reference (*.asc)'].split(',')
            tele_id = row["Tele ID"]
            for part in parts:
                part = part.strip()
                tele_components[part] = tele_id.strip()


def main():
    start_time = time.time()

    setup()

    get_components("axiom_beta_main_board_v0.38_r1.2", "_MB", frame_width + cutout_width * 2 + 57.15,
                   57.15 + frame_width + cutout_width * 2)
    get_components("axiom_beta_power_board_v0.38_r1.2b", "_PB", 57.15 + frame_width + cutout_width * 2,
                   frame_width + cutout_width)
    get_components("axiom_beta_interface_dummy_v0.13_r1.6", "_IB", frame_width + cutout_width,
                   frame_width + cutout_width, True)
    get_components("axiom_beta_sensor_cmv12000_tht_v0.16_r1.8c", "_SB", frame_width + cutout_width,
                   57.15 + frame_width + cutout_width * 2, True)

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

    draw_component_positions(OUTPUT_DIR + "pnp_data_top.asc", drawing_top)
    drawing_top.savePng(OUTPUT_DIR + "pnp_output_top.png")

    draw_component_positions(OUTPUT_DIR + "pnp_data_bottom.asc", drawing_bottom, True)
    drawing_bottom.savePng(OUTPUT_DIR + "pnp_output_bottom.png")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

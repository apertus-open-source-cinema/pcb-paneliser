import os
import time
from math import radians
from xml.etree import ElementTree

import ezdxf
import gerberex
from gerberex import GerberComposition
from progressbar import ProgressBar

INPUT_DIR = "input/base_variant/"
OUTPUT_DIR = "output_stage1_pnp/"
EAGLE_DATA_DIR = "input/EAGLE/"
TEMP_DIR = "temp/"

elements = []

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


board_context = GerberComposition(settings=GerberSettings)
component_context = GerberComposition(settings=GerberSettings)

processes = []


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


count = 0


# def process(fn):
#    @wraps(fn)
#    def increase_count(*args, **kwargs):
#        global count
#        count += 1
#        return fn(*args, **kwargs), count

# processes.append(fn)

# return increase_count

# @functools.wraps
# def test():
#    print("test1")
# fn()
# processes.append(fn)


# @process
def test1():
    print("test1")


# @process
def test2():
    print("test2")


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


# @process
def get_elements(pcb_name, suffix, offset_x, offset_y, rotated=False):
    brd_path = EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".brd"
    tree = ElementTree.parse(brd_path)
    xml_root = tree.getroot()
    board_x, board_y, board_width, board_height, board_offset_x, board_offset_y = get_board_dimensions(xml_root)
    # board_data = gerberex.read(INPUT_DIR + pcb_name + "/" + pcb_name + ".boardoutline.ger")
    # board_outline = gerberex.read(INPUT_DIR + pcb_name + "/" + pcb_name + ".boardoutline.ger")
    # board_outline.to_metric()
    # board_width = float(board_outline.size[0])
    # board_height = float(board_outline.size[1])

    # board_offset_x = board_outline.bounds[0][0]
    # board_offset_y = board_outline.bounds[1][0]

    if rotated:
        board_width, board_height = board_height, board_width
        board_offset_x, board_offset_y = board_offset_y, board_offset_x
    # board_offset_x, board_offset_y = board_offset_y, board_offset_x

    file = open(EAGLE_DATA_DIR + pcb_name + "/" + pcb_name + ".mnt", "r")
    for line in file:
        name, x, y, rotation, *temp = line.split()
        if rotated:
            x, y = -float(y), x
            rotation = int(rotation) + 90

        x = float(x) + offset_x + board_width / 2 + board_offset_x / 2  # + board_width / 2  # - board_offset_x
        y = float(
            y) + offset_y + board_height / 2 + board_offset_y / 2  # + (60.96 - 50.8) / 2  # + board_height / 2  # + board_offset_y
        elements.append((name, x, y, rotation))
        # and let's extract the data:
        # songTitle = fields[0]
        # artist = fields[1]
        # duration = fields[2]

        # Print the song
        print(name + suffix, x, y, rotation,
              temp)  # songTitle + " by " + artist + " Duration: " + duration)


def draw_component_positions(board_file_path):
    for element in elements:
        name, x, y, rotation, *temp = element
        board_cutout_msp.add_lwpolyline([(0.0, 0.0), (0.0, 0.3)], format="xy").rotate_z(
                radians(int(rotation))).translate(x, y, 0)
        board_cutout_msp.add_circle((x, y), 0.2)
        # board_cutout_msp.add_lwpolyline([(0.0, 0.0), (100.0, 100.0)], dxfattribs={'linetype': 'DASHED'})


def write_origin():
    pass


def write_component_positions():
    pass


def main():
    start_time = time.time()

    # ctx = GerberCairoContext(scale=50)

    # top_layer = gerberex.read('output_stage1/axiom_beta_mixed_panel.topcream.ger')
    # board_context.merge(top_layer)
    # board_outline = gerberex.read('output_stage1/WITH_OUTLINE_axiom_beta_mixed_panel.boardoutline.ger')
    # board_context.merge(board_outline)
    # board_context.dump(OUTPUT_DIR + "pnp_background.ger")

    # background_layer = load_layer(OUTPUT_DIR + "pnp_background.ger")
    # ctx.render_layer(background_layer)

    # ctx.dump("test.png")

    file = open("pnp_data.asc", "w")

    bar = ProgressBar()
    bar.start()
    setup()

    get_elements("axiom_beta_main_board_v0.37_r1.1", "_1", 7.5, 10 + 57.15, True)  # 7.5 + 57.15

    get_elements("axiom_beta_power_board_v0.37_r1.2", "_2",
                 57.15 + 10, 57.15 + 10, True)

    get_elements("axiom_beta_interface_dummy_v0.13_r1.3", "_3", 10 + 57.15, 7.5)

    get_elements("axiom_beta_sensor_cmv12000_tht_v0.16_r1.5c", "_4", 7.5, 7.5)

    # board_cutout_doc.linetypes.new('GASLEITUNG2', dxfattribs={
    #    'description': 'Gasleitung2 ----GAS----GAS----GAS----GAS----GAS----GAS--',
    #    'length': 1,  # required for complex line types
    #    # line type definition in acadlt.lin:
    #    'pattern': 'A,.5,-.2,["GAS",STANDARD,S=.1,U=0.0,X=-0.1,Y=-.05],-.25',
    # })

    draw_component_positions(
            "input/axiom_beta_power_board_v0.37_r1.2/axiom_beta_power_board_v0.37_r1.2.boardoutline.ger")

    # draw_component_positions(INPUT_DIR + "axiom_beta_power_board_v0.37_r1.2.mnb",
    #    "input/axiom_beta_power_board_v0.37_r1.2/axiom_beta_power_board_v0.37_r1.2.boardoutline.ger")

    board_cutout_doc.saveas("test.dxf")

    dxf = gerberex.read('test.dxf')
    component_context.merge(dxf)
    component_context.dump(OUTPUT_DIR + "component_position.ger")
    # bar.update()
    # elements2 = get_elements(INPUT_DIR + "axiom_beta_power_board_v0.37_r1.2.mnt")
    # bar.update()

    write_origin()
    write_component_positions()

    # for i in progressbar.progressbar(range(100), redirect_stdout=True):
    #    print('Some text', i)
    #    time.sleep(0.01)

    # for i in range(len(processes)):
    #    processes[i]()
    #   bar.update(i)
    # bar.update(7)
    # bar.update(21)

    # index = 0
    # for proc in processes:
    #    proc()
    #    bar.update(index)
    #    index += 1

    # print(test1())
    # print(test1())
    # print(test1())

    # print(test2())
    # print(test2())

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")
    bar.finish()


if __name__ == "__main__":
    # execute only if run as a script
    main()

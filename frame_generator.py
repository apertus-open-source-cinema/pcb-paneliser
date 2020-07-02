from shapely.geometry import MultiLineString, box

from dxf_helper import create_dxf_rectangle


def generate_outer_frame(dxf_modelspace, width, height):  # bridge_count_vertical, bridge_count_horizontal):
    create_dxf_rectangle(dxf_modelspace, 0, 0, width, height)
    # frame_lines = MultiLineString(cutout_lines)
    # dilated = frame_lines.buffer(cnc_cutout_half_width)

    # for element in dilated:
    # dxf_modelspace.add_lwpolyline(dilated.exterior.coords)


bridge_width = 5  # mm

cutout_lines = []
splitter_rectangles = []


def generate_pcb_frame(dxf_modelspace, x, y, width, height,
                       cutout_width):  # bridge_count_vertical, bridge_count_horizontal):
    cutout_half_width = cutout_width / 2
    x -= cutout_half_width
    y -= cutout_half_width
    width += cutout_width
    height += cutout_width
    cutout_lines.append([(x, y), (x + width, y), (x + width, y + height),
                         (x, y + height), (x, y)])

    # create_dxf_rectangle(dxf_modelspace, x - cutout_width / 2, y - cutout_width / 2, width + cutout_width,
    #                     height + cutout_width)
    frame_lines = MultiLineString(cutout_lines)
    # dilated = frame_lines.buffer(cutout_half_width)

    # for element in frame_lines:
    #    dxf_modelspace.add_lwpolyline(element.coords)


def __generate_horizontal_splitters(dxf_modelspace, area_y, area_height, length, width, count):
    splitter_distance = area_height - area_y
    splitter_distance /= (count + 1)

    half_height = width / 2

    for y in range(1, count + 1):
        rectangle = box(0, y * splitter_distance - half_height, length, y * splitter_distance + half_height)
        splitter_rectangles.append(rectangle)
        # dxf_modelspace.add_lwpolyline(rectangle.exterior.coords)


def __generate_vertical_splitters(dxf_modelspace, area_x, area_width, length, width, count):
    splitter_distance = area_width - area_x
    splitter_distance /= (count + 1)

    half_width = width / 2

    for x in range(1, count + 1):
        rectangle = box(x * splitter_distance - half_width, 0, x * splitter_distance + half_width, length)
        splitter_rectangles.append(rectangle)
        #dxf_modelspace.add_lwpolyline(rectangle.exterior.coords)


def __generate_bridges(dxf_modelspace, area, count_x, count_y):
    # rectangle = box(5, 10, 140, 15)

    area_x = area[0]
    area_y = area[1]
    area_width = area[2]
    area_height = area[3]

    __generate_horizontal_splitters(dxf_modelspace, area_y, area_height, area_width, bridge_width, count_y)
    __generate_vertical_splitters(dxf_modelspace, area_x, area_width, area_height, bridge_width, count_x)

    # splitter_rectangles.append(rectangle)
    # dxf_modelspace.add_lwpolyline(rectangle.exterior.coords)


def generate_pcb_bridges(dxf_modelspace, area, cutout_width, count_x, count_y):
    __generate_bridges(dxf_modelspace, area, count_x, count_y)

    frame_lines = MultiLineString(cutout_lines)
    # bridge_lines = MultiLineString(splitter_rectangles)
    # bridge_lines2 = bridge_lines.union(bridge_lines)
    for splitter in splitter_rectangles:
        frame_lines = frame_lines.difference(splitter)
    dilated = frame_lines.buffer(cutout_width / 2)

    for element in dilated:
        dxf_modelspace.add_lwpolyline(element.exterior.coords)

# for element in frame_lines:
#    dxf_modelspace.add_lwpolyline(element.coords)

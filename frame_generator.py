from shapely import geometry, ops
from shapely.geometry import MultiLineString, box, LineString

from dxf_helper import create_dxf_rectangle

bridge_width = 5  # mm

cutout_lines = []
splitter_rectangles = []


def generate_outer_frame(dxf_modelspace, width, height):  # bridge_count_vertical, bridge_count_horizontal):
    create_dxf_rectangle(dxf_modelspace, 0, 0, width, height)


def generate_pcb_frame(dxf_modelspace, x, y, width, height,
                       cutout_width):  # bridge_count_vertical, bridge_count_horizontal):
    cutout_half_width = cutout_width / 2
    x -= cutout_half_width
    y -= cutout_half_width
    width += cutout_width
    height += cutout_width
    cutout_lines.append([(x, y), (x + width, y), (x + width, y + height),
                         (x, y + height), (x, y)])


def __generate_horizontal_splitters(dxf_modelspace, area_y, area_height, length, width, count):
    splitter_distance = area_height - area_y
    splitter_distance /= (count + 1)

    half_height = width / 2

    for y in range(1, count + 1):
        rectangle = box(0, y * splitter_distance - half_height, length, y * splitter_distance + half_height)
        splitter_rectangles.append(rectangle)


def __generate_vertical_splitters(dxf_modelspace, area_x, area_width, length, width, count):
    splitter_distance = area_width - area_x
    splitter_distance /= (count + 1)

    half_width = width / 2

    for x in range(1, count + 1):
        rectangle = box(x * splitter_distance - half_width, 0, x * splitter_distance + half_width, length)
        splitter_rectangles.append(rectangle)


def __generate_bridges(dxf_modelspace, area, count_x, count_y):
    area_x = area[0]
    area_y = area[1]
    area_width = area[2]
    area_height = area[3]

    __generate_horizontal_splitters(dxf_modelspace, area_y, area_height, area_width, bridge_width, count_y)
    __generate_vertical_splitters(dxf_modelspace, area_x, area_width, area_height, bridge_width, count_x)


def generate_pcb_bridges(dxf_modelspace, area, cutout_width, count_x, count_y):
    __generate_bridges(dxf_modelspace, area, count_x, count_y)

    frame_lines = MultiLineString(cutout_lines)

    for splitter in splitter_rectangles:
        frame_lines = frame_lines.difference(splitter)

    dilated = frame_lines.buffer(cutout_width / 2)

    for element in dilated:
        dxf_modelspace.add_lwpolyline(element.exterior.coords)


def generate_subpanel_bridges(dxf_outline_space, dxf_drill_space, area, cutout_width, count_x, count_y):
    __generate_bridges(dxf_outline_space, area, count_x, count_y)

    frame_lines = MultiLineString(cutout_lines)

    generate_mouse_bites(area, dxf_drill_space, frame_lines)

    for splitter in splitter_rectangles:
        frame_lines = frame_lines.difference(splitter)

    # Merge all lines, so the endpoints are not where lines cross
    frame_lines = ops.linemerge(frame_lines)

    inset_lines = []
    for frame_line in frame_lines:
        line = frame_line.parallel_offset(2, 'left')

        # line2 = frame_line.parallel_offset(2, 'right')
        if frame_line.boundary and line.boundary:
            inset_line = LineString([frame_line.boundary[0], line.boundary[0]])
            inset_lines.append(inset_line)
            inset_line = LineString([frame_line.boundary[1], line.boundary[1]])
            inset_lines.append(inset_line)

        line = frame_line.parallel_offset(2, 'right')
        if frame_line.boundary and line.boundary:
            inset_line = LineString([frame_line.boundary[0], line.boundary[1]])
            inset_lines.append(inset_line)
            inset_line = LineString([frame_line.boundary[1], line.boundary[0]])
            inset_lines.append(inset_line)

        # frame_lines = frame_lines.union(inset_line)

    inset_lines = MultiLineString(inset_lines)
    dilated_insets = inset_lines.buffer(cutout_width / 3, join_style=1)

    # Remove outward bridges TODO: Needs better solution, this one is a quick hack TODO: Check if interior exterior
    #  of polygon would work: https://gis.stackexchange.com/questions/341604/creating-shapely-polygons-with-holes
    # dilated_insets = clean_outer_perimeter(area, dilated_insets)

    # Merge cutouts and insets
    dilated = frame_lines.buffer(cutout_width / 2, cap_style=2, join_style=2)
    dilated = dilated.union(dilated_insets)
    # Round the corners of insets
    dilated = dilated.buffer(0.8, join_style=1).buffer(-0.8, join_style=1)
    for element in dilated:
        dxf_outline_space.add_lwpolyline(element.exterior.coords)


def generate_mouse_bites(area, dxf_drill_space, frame_lines):
    bridge_box = geometry.box(area[0], area[1], area[2], area[3])
    for splitter in splitter_rectangles:
        bridge_box = bridge_box.difference(splitter)

    bridge_box = bridge_box.buffer(1)

    bridge_lines = frame_lines
    for splitter in bridge_box:
        bridge_lines = bridge_lines.difference(splitter)

    for element in bridge_lines:
        # if type(element) is LineString:
        element_right = element.parallel_offset(2, 'right')
        dxf_drill_space.add_lwpolyline(element_right.coords)
        element_left = element.parallel_offset(2, 'left')
        dxf_drill_space.add_lwpolyline(element_left.coords)

    return frame_lines


def clean_outer_perimeter(area, dilated_insets):
    outer_rectangle = geometry.box(area[0], area[1], area[2], 5)
    outer_rectangle = outer_rectangle.union(geometry.box(area[0], area[1], 5, area[3]))
    outer_rectangle = outer_rectangle.union(geometry.box(area[0], area[3] - 5, area[2], area[3]))
    outer_rectangle = outer_rectangle.union(geometry.box(area[2] - 5, area[1], area[2], area[3]))
    dilated_insets = dilated_insets.difference(outer_rectangle)
    return dilated_insets

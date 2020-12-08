import os
from pathlib import Path
from xml.etree import ElementTree

import ezdxf
import gerberex
from gerberex import GerberComposition

INPUT_DIR = Path("input/EAGLE/axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c/")
OUTPUT_DIR = Path("output_impedance_stage1")

trace_doc = ezdxf.new('R2010')
trace_msp = trace_doc.modelspace()

cutout_width = 2.54  # mm
frame_width = 5  # mm

sb_width = 57.15
sb_height = 57.15


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

traces_gerber = GerberComposition(settings=GerberSettings)


def main():

    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76

    width = 0
    tree = ElementTree.parse(INPUT_DIR / "axiom_beta_sensor_cmv12000_tht_v0.16_r1.6c.brd")
    xml_root = tree.getroot()
    lvds_signals = xml_root.findall(".//signal[@class=\"1\"]")
    for signal in lvds_signals:
        traces = signal.findall(".//wire[@layer=\"1\"]")
        for trace in traces:
            x1, y1 = trace.attrib["x1"], trace.attrib["y1"]
            x2, y2 = trace.attrib["x2"], trace.attrib["y2"]
            width = float(trace.attrib["width"])
            curve = 0
            if "curve" in trace.attrib:
                curve = float(trace.attrib["curve"])
            trace_msp.add_lwpolyline([(float(x1) + frame_width + cutout_width + sb_width/2, float(y1) + frame_width + cutout_width + sb_height/2, 
                width, curve / 180.0), (float(x2) + frame_width  + cutout_width + sb_width/2, float(y2) + frame_width + cutout_width + sb_height/2)],
                                     format='xysb')

    trace_doc.saveas("impedance.toplayer.dxf")
    dxf = gerberex.read("impedance.toplayer.dxf")
    dxf.width = width
    traces_gerber.merge(dxf)
    traces_gerber.dump(OUTPUT_DIR / "impedance.toplayer.ger")


if __name__ == "__main__":
    # execute only if run as a script
    main()

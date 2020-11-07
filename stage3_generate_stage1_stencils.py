import os
import time

import ezdxf
import gerberex
from gerberex import GerberComposition

TEMPLATE_DIR = "input/elements/"
INPUT_DIR = "output_stage1/"
OUTPUT_DIR = "output_stage3/"

cutout_width = 2.5  # mm
frame_width = 5  # mm

board_cutout_doc = ezdxf.new('R2010')
board_cutout_msp = board_cutout_doc.modelspace()


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


stencil_context = GerberComposition(settings=GerberSettings)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def place_fiducial(x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(TEMPLATE_DIR + "fiducial_2.30mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    stencil_context.merge(fiducial)


def main():
    start_time = time.time()

    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76

    # Top layer
    cream_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.topcream.ger")
    cream_layer.to_metric()
    stencil_context.merge(cream_layer)

    # Top fiducials
    place_fiducial(2.5, 2.5)
    place_fiducial(panel_width - 2.5, 2.5)
    place_fiducial(2.5, panel_height - 2.5)
    place_fiducial(panel_width - 2.5, panel_height - 2.5)

    # Bottom layer
    offset = 170
    cream_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.bottomcream.ger")
    cream_layer.to_metric()
    cream_layer.offset(offset)
    stencil_context.merge(cream_layer)

    # Bottom fiducials
    place_fiducial(offset + 2.5, 2.5)
    place_fiducial(offset + panel_width - 2.5, 2.5)
    place_fiducial(offset + 2.5, panel_height - 2.5)
    place_fiducial(offset + panel_width - 2.5, panel_height - 2.5)

    stencil_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel.stencil.ger")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

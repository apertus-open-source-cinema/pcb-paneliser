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
engrave_context = GerberComposition(settings=GerberSettings)
copper_context = GerberComposition(settings=GerberSettings)
soldermask_context = GerberComposition(settings=GerberSettings)


def setup():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)





def main():
    start_time = time.time()

    setup()

    panel_width = frame_width * 2 + cutout_width * 3 + 57.15 * 2
    panel_height = frame_width * 2 + cutout_width * 3 + 57.15 + 111.76

    # Top layer
    cream_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.topcream.ger")
    cream_layer.to_metric()
    stencil_context.merge(cream_layer)

    engrave_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.topengrave.ger")
    engrave_layer.to_metric()
    engrave_context.merge(engrave_layer)

    copper_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.toplayer.ger")
    copper_layer.to_metric()
    copper_context.merge(copper_layer)

    soldermask_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.topsoldermask.ger")
    soldermask_layer.to_metric()
    soldermask_context.merge(soldermask_layer)



    # Bottom layer
    offset = 210
    cream_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.bottomcream-mirrored.ger")
    cream_layer.to_metric()
    cream_layer.offset(offset)
    stencil_context.merge(cream_layer)

    engrave_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.bottomengrave-mirrored.ger")
    engrave_layer.to_metric()
    engrave_layer.offset(offset)
    engrave_context.merge(engrave_layer)

    copper_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.bottomlayer-mirrored.ger")
    copper_layer.to_metric()
    copper_layer.offset(offset)
    copper_context.merge(copper_layer)

    soldermask_layer = gerberex.read(INPUT_DIR + "axiom_beta_mixed_panel.bottomsoldermask-mirrored.ger")
    soldermask_layer.to_metric()
    soldermask_layer.offset(offset)
    soldermask_context.merge(soldermask_layer)


    stencil_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel_stencil.cut.ger")
    engrave_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel_stencil.engrave.ger")
    copper_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel_stencil.copper.ger")
    soldermask_context.dump(OUTPUT_DIR + "axiom_beta_mixed_panel_stencil.soldermask.ger")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("\r\nElapsed time: %.2f" % elapsed_time, "seconds")


if __name__ == "__main__":
    # execute only if run as a script
    main()

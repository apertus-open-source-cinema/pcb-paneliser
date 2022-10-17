from datetime import date

import gerberex
from HersheyFonts import HersheyFonts

import pcb_panel_config as cfg
from pcb_scripts.pcb_panel_info import PCBPanel

font = HersheyFonts()
font.load_default_font()


def draw_text(model_space, text, x, y, rotated=False):
    for (x1, y1), (x2, y2) in font.lines_for_text(text):
        if rotated:
            x1, y1, x2, y2 = -y1, x1, -y2, x2

        x1, y1, x2, y2 = x1 + x, y1 + y, x2 + x, y2 + y

        model_space.add_lwpolyline([(x1, y1), (x2, y2)],
                                   format='xy')


def place_panel_label(pcb_panel, x, y):
    # silk screen label
    label = gerberex.read(cfg.ELEMENTS_DIR + "panel_label.gbr")
    label.to_metric()
    label.offset(x, y)
    pcb_panel.silkscreen_top_layer.merge(label)


def place_subpanel_label(model_space, text, x, y):
    today = date.today()
    font.normalize_rendering(2)
    # previous version: "AXIOM Beta Mixed Subpanel - Version 0.43
    label_text = f"{text} - Date: " + today.strftime("%d.%m.%Y") + " (DD.MM.YYYY)"
    draw_text(model_space, label_text, x, y, True)


def place_top_fiducial(pcb_panel: PCBPanel, x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "fiducial_2.30mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.soldermask_top_layer.merge(fiducial)

    # Copper fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.copper_layer_top.merge(fiducial)


def place_top_origin(pcb_panel: PCBPanel, x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "origin_1.12mm_dia_circle_soldermask.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.soldermask_top_layer.merge(fiducial)

    # Copper cross
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "origin_cross.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.copper_layer_top.merge(fiducial)


def place_bot_fiducial(pcb_panel: PCBPanel, x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "fiducial_2.30mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.soldermask_bot_layer.merge(fiducial)

    # Copper fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "fiducial_1.20mm_dia_circle.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.copper_layer_bot.merge(fiducial)


def place_bot_origin(pcb_panel: PCBPanel, x, y):
    # Solder mask fiducial
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "origin_1.12mm_dia_circle_soldermask.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.soldermask_bot_layer.merge(fiducial)

    # Copper cross
    fiducial = gerberex.read(cfg.ELEMENTS_DIR + "origin_cross.gbr")
    fiducial.to_metric()
    fiducial.offset(x, y)
    pcb_panel.copper_layer_bot.merge(fiducial)

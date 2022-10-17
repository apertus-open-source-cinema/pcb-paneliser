from dataclasses import dataclass

from gerberex import GerberComposition, DrillComposition


class GerberSettings:
    format = [3, 3]
    units = "metric"
    zero_suppression = "leading"


class DrillSettings:
    format = [3, 3]
    units = "metric"
    zeros = "trailing"
    notation = "absolute"
    zero_suppression = "leading"


@dataclass
class PCBPanel:
    board_outline = GerberComposition(settings=GerberSettings)
    copper_layer_top = GerberComposition(settings=GerberSettings)
    soldermask_top_layer = GerberComposition(settings=GerberSettings)
    silkscreen_top_layer = GerberComposition(settings=GerberSettings)
    copper_layer_bot = GerberComposition(settings=GerberSettings)
    soldermask_bot_layer = GerberComposition(settings=GerberSettings)
    silkscreen_bot_layer = GerberComposition(settings=GerberSettings)
    cream_top_layer = GerberComposition(settings=GerberSettings)
    cream_bot_layer = GerberComposition(settings=GerberSettings)
    internalplane1_layer = GerberComposition(settings=GerberSettings)
    internalplane2_layer = GerberComposition(settings=GerberSettings)

    drills = DrillComposition(settings=DrillSettings)
